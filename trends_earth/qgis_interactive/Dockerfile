# Use the jlesage/baseimage-gui:ubuntu-22.04-v4 as base image
FROM jlesage/baseimage-gui:ubuntu-22.04-v4 AS build

MAINTAINER Bjoern Gruening, bjoern.gruening@gmail.com

RUN apt-get update -y && \
     DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
         ca-certificates \
         wget \
         libgl1 \
         qt5dxcb-plugin && \
     rm -rf /var/lib/apt/lists/*

COPY startapp.sh /startapp.sh
RUN chmod +x /startapp.sh && \
    mkdir -p /app/qgis

# ... (rest of your Dockerfile)

# Set the name of the application.
ENV APP_NAME="QGIS"

ENV KEEP_APP_RUNNING=0

ENV TAKE_CONFIG_OWNERSHIP=1

# Set environment
ENV JAVA_HOME /opt/jdk
ENV PATH ${PATH}:${JAVA_HOME}/bin
WORKDIR /app/qgis

USER root
RUN apt-get update && apt-get install -y gnupg software-properties-common

# Install required packages for X11 and QGIS
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    x11-apps \
    qgis qgis-plugin-grass

# Set the DISPLAY environment variable to point to the X11 server on the host (not working for now)
#ENV DISPLAY=host.docker.internal:0

# Share the X11 socket with the container (same here)
#VOLUME /tmp/.X11-unix:/tmp/.X11-unix

WORKDIR /config

