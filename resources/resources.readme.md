# Resources for Jupyterhub

## `jupyterhub_config.reference.py`.

All available settings for jupyterhub can be referenced here.
This file is generated using `jupyterhub --generate-config`.

## `Dockerfile.user`

A docker image template is used to start new containers for each users.
The current configuration is to pull from official jupyter docker repository
`quay.io/jupyter/minimal-notebook:latest`.

In the future, we can set multiple choices for users to choose which image
to start from. Images to be designed in the future can be further modified
from this `Dockefile.user` as a template starter. For example, we can
preinstall datascience libraries `pip install -r requirements.user.txt`.
