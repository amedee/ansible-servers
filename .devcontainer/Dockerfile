FROM mcr.microsoft.com/devcontainers/python:3.14

COPY apt-packages.txt /tmp/apt-packages.txt

RUN apt-get update \
 && xargs -a /tmp/apt-packages.txt apt-get install -y --no-install-recommends \
 && rm -rf /var/lib/apt/lists/* \
 && rm -f /tmp/apt-packages.txt
