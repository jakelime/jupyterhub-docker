ARG url_docker=docker.io
ARG url_pypi=https://pypi.org/simple/
FROM ${url_docker}/python:3.12.11-bookworm

ARG url_pypi
ENV url_pypi=${url_pypi}

RUN python3 -m pip install --upgrade jupyterlab --index-url ${url_pypi}
RUN python3 -m pip install --upgrade notebook --index-url ${url_pypi}