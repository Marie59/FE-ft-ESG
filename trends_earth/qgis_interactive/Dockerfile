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
ENV APP_VERSION="3.32"

ENV KEEP_APP_RUNNING=0

ENV TAKE_CONFIG_OWNERSHIP=1

# Set environment
ENV JAVA_HOME /opt/jdk
ENV PATH ${PATH}:${JAVA_HOME}/bin
WORKDIR /app/qgis

USER root

# Install required packages for X11 and QGIS
RUN DEBIAN_FRONTEND=noninteractive apt update && apt install wget gnupg -y && \
    wget -O - https://qgis.org/downloads/qgis-2022.gpg.key | gpg --import && \
    gpg --export --armor D155B8E6A419C5BE | apt-key add - && \
    apt-get update && apt-get install -y qgis qgis-plugin-grass && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /config
