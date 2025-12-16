# Configuration file for jupyterhub.

import os

import nativeauthenticator

try:
    JUPYTERHUB_PORT = int(os.getenv("JUPYTERHUB_PORT"))
except Exception as e:
    print(f"{e=}")
    JUPYTERHUB_PORT = 8001


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
c.Authenticator.admin_users = {
    "jfroot",
}
c.Authenticator.allow_all = True

# --- Spawner (Docker) ---
c.JupyterHub.spawner_class = "dockerspawner.DockerSpawner"

# The Docker Network.
c.DockerSpawner.network_name = "jetforge-docker_jf_net"

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
c.JupyterHub.db_url = "sqlite:////srv/jupyterhub/jupyterhub.sqlite"


# --- Resource management configurations ---
c.JupyterHub.shutdown_on_logout = True
c.JupyterHub.active_server_limit = 10
c.JupyterHub.named_server_limit_per_user = 2