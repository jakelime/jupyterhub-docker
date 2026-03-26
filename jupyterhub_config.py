# Configuration file for jupyterhub.

import os
import re
from pathlib import Path

import nativeauthenticator

try:
    JUPYTERHUB_PORT = int(os.getenv("JUPYTERHUB_PORT"))
except Exception as e:
    print(f"{e=}")
    JUPYTERHUB_PORT = 8001

DOCKER_NETWORK_NAME = os.getenv("DOCKER_NETWORK_NAME", "jetforge-docker_jf_net")


def sanitize_username(username: str) -> str:
    """Keep only '.', '_', and alphanumeric characters (removes spaces, etc)."""
    results = re.sub(r"[^a-zA-Z0-9._]", "", username)
    return results.lower()


_admin_users = os.getenv("ADMIN_USERS", "jujuadmin,jujuroot")
ADMIN_USERS = set(
    sanitize_username(user) for user in _admin_users.split(",") if sanitize_username(user)
)

c = get_config()

# --- Network & URL Configuration ---
# Reverse proxy setup using nginx to route /jupyterhub/ to JupyterHub
c.JupyterHub.base_url = "/jupyterhub"

# Listen on all interfaces
c.JupyterHub.hub_ip = "0.0.0.0"
c.JupyterHub.hub_port = JUPYTERHUB_PORT

# --- Authentication ---
c.JupyterHub.authenticator_class = "native"
c.JupyterHub.template_paths = [
    f"{os.path.dirname(nativeauthenticator.__file__)}/templates/"
]
c.Authenticator.admin_users = ADMIN_USERS
c.Authenticator.allow_all = True

# --- Spawner (Docker) ---
c.JupyterHub.spawner_class = "dockerspawner.DockerSpawner"

# The Docker Network.
c.DockerSpawner.network_name = DOCKER_NETWORK_NAME

# How spawned containers reach the Hub
c.DockerSpawner.hub_connect_url = f"http://jupyterhub:{JUPYTERHUB_PORT}"
c.DockerSpawner.use_internal_ip = True

# Container settings
c.DockerSpawner.image = "quay.io/jupyter/minimal-notebook:python-3.13.11"
c.DockerSpawner.pull_policy = "ifnotpresent"
c.DockerSpawner.remove = True  # Delete container when server stops
c.Spawner.mem_limit = "2G"

# --- User Persistence ---
# Map a volume so users don't lose files when their container restarts
# jovyan is the default user in jupyter/minimal-notebook image
notebook_dir = os.environ.get("NOTEBOOK_DIR") or "/home/jovyan/work"
c.DockerSpawner.notebook_dir = notebook_dir
c.DockerSpawner.volumes = {"jupyterhub-user-{username}": notebook_dir}

# --- Data Persistence ---
# Persist the Hub database
# c.JupyterHub.db_url = "sqlite:////srv/jupyterhub/jupyterhub.sqlite"
datashare_dir = Path(os.getenv("DATASHARE_DIR", "/datashare")) / "jupyterhub"
datashare_dir.mkdir(parents=True, exist_ok=True)
c.JupyterHub.db_url = "sqlite:////datashare/jupyterhub/jupyterhub.sqlite"


# --- Resource management configurations ---
c.JupyterHub.shutdown_on_logout = True
c.JupyterHub.active_server_limit = 10
c.JupyterHub.named_server_limit_per_user = 2
