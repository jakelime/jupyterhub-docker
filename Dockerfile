ARG url_docker=docker.io
ARG url_pypi=https://pypi.org/simple/
FROM ${url_docker}/jupyterhub/jupyterhub:5.4.3

ARG url_pypi
ENV url_pypi=${url_pypi}

COPY jupyterhub_config.py /etc/jupyterhub/jupyterhub_config.py
COPY requirements.txt /etc/jupyterhub/requirements.txt
RUN pip install -r /etc/jupyterhub/requirements.txt --index-url ${url_pypi}
