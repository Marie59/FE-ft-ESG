FROM dorowu/ubuntu-desktop-lxde-vnc

USER root

# RUN apt-get install Xviewer
RUN wget http://archive.ubuntu.com/ubuntu/pool/main/s/screen/screen_4.6.2-1_amd64.deb


# Download the ODV code.

# For now, we use a local copy. The software itself is behind a login-wall and needs a solution.
#RUN wget 'http://.../odv_5.6.5_linux-amd64.tar.gz'
#RUN wget 'http://.../run_odv'
RUN mkdir -p /app/odv
WORKDIR /app/odv
COPY './odv_5.6.5_linux-amd64.tar.gz' ./odv.tar.gz
RUN tar -xvzf odv.tar.gz &&  \
    rm odv.tar.gz

WORKDIR /root/Desktop
COPY --chmod=755 './run_odv' ./run_odv

ENTRYPOINT []
CMD []




