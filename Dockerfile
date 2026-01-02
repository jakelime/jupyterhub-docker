ARG URL_DOCKER_INDEX=docker.io
ARG URL_PYPI_INDEX=https://pypi.org/simple/
FROM ${URL_DOCKER_INDEX}/jupyterhub/jupyterhub:5.4.3

ARG URL_PYPI_INDEX
ENV URL_PYPI_INDEX=${URL_PYPI_INDEX}

COPY jupyterhub_config.py /etc/jupyterhub/jupyterhub_config.py
COPY requirements.txt /etc/jupyterhub/requirements.txt
RUN pip install -r /etc/jupyterhub/requirements.txt --index-url ${URL_PYPI_INDEX}
