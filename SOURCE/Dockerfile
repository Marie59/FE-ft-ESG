FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu20.04

ENV NB_USER="gpuuser"
ENV UID=999

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends \
    git \
    ca-certificates \
    software-properties-common \
    locales \
    gcc pkg-config libfreetype6-dev libpng-dev g++ \
    pandoc \
    sudo \
    curl \
    libffi-dev \
    net-tools \
    wget

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt-get update && \
    apt install -y python3.8 python3.8-dev python3-pip python3.8-distutils gfortran libopenblas-dev liblapack-dev

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1 \
    && update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1
 
RUN alias python=/usr/bin/python3.8
   
RUN python3.8 -m pip install --upgrade pip requests setuptools pipenv

ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt

ENV PATH=/usr/bin/python3.8:$PATH

ENV CONDA_DIR=/opt/conda \
    SHELL=/bin/bash \
    NB_USER="${NB_USER}" \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8 \
    PATH="${CONDA_DIR}/bin:${PATH}" \
    HOME="/home/${NB_USER}"

RUN echo "auth requisite pam_deny.so" >> /etc/pam.d/su && \
    sed -i.bak -e 's/^%admin/#%admin/' /etc/sudoers && \
    sed -i.bak -e 's/^%sudo/#%sudo/' /etc/sudoers && \
    useradd -l -m -s /bin/bash -u $UID $NB_USER && \
    mkdir -p "${CONDA_DIR}" && \
    chown -R "${NB_USER}" "${CONDA_DIR}" && \
    chmod g+w /etc/passwd

USER ${NB_USER}

ENV PATH=$CONDA_DIR/bin:$PATH
ENV PATH=/home/$NB_USER/.local/bin:$PATH

RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -f -b -p /opt/conda && rm -rf ~/miniconda.sh

RUN conda install -c conda-forge mamba python==3.8
RUN mamba install -y -q -c "nvidia/label/cuda-11.8.0" cuda-nvcc
RUN conda install -c conda-forge source

RUN python3.8 -m pip install \
    bioblend==1.0.0 \
    galaxy-ie-helpers==0.2.7 \
    numba==0.56.4 \
    aquirdturtle_collapsible_headings==3.1.0 \
    jupyterlab-nvdashboard==0.7.0 \
    bokeh==2.4.0 \
    jupyter_server==1.16.0 \
    jupyterlab==3.4.6 \
    nbclassic==0.4.8 \
    jupyterlab-git==0.39.3 \
    jupytext==1.14.1 \
    jupyterlab-execute-time==2.3.0 \
    jupyterlab-kernelspy==3.1.0 \
    jupyterlab-system-monitor==0.8.0 \
    jupyterlab-topbar==0.6.1 \

RUN sed -i -e "s/jax.tree_flatten/jax.tree_util.tree_flatten/g" /opt/conda/lib/python3.8/site-packages/alphafold/model/mapping.py
RUN sed -i -e "s/jax.tree_unflatten/jax.tree_util.tree_unflatten/g" /opt/conda/lib/python3.8/site-packages/alphafold/model/mapping.py

RUN python3.8 -m pip install \
    tensorflow-gpu==2.7.0 \
    tensorflow_probability==0.15.0

USER root 

RUN mkdir -p /home/$NB_USER/.ipython/profile_default/startup/
RUN mkdir -p /import
RUN mkdir -p /home/$NB_USER/.jupyter/custom/ && \
RUN mkdir -p /home/$NB_USER/notebooks

COPY ./startup.sh /startup.sh
COPY ./get_notebook.py /get_notebook.py

COPY ./galaxy_script_job.py /home/$NB_USER/.ipython/profile_default/startup/00-load.py
COPY ./ipython-profile.py /home/$NB_USER/.ipython/profile_default/startup/01-load.py
COPY ./jupyter_notebook_config.py /home/$NB_USER/.jupyter/

COPY ./*.ipynb /home/$NB_USER/

COPY ./notebooks/*.ipynb /home/$NB_USER/notebooks/
    
# Download notebooks
RUN cd   /home/$NB_USER/;  \
    wget -O test_docker.zip https://github.com/fair-ease/Source/archive/refs/heads/test_docker.zip; unzip test_docker.zip; \
    rm /home/$NB_USER/test_docker.zip
 
RUN mv /home/$NB_USER/Source-test_docker/notebooks /home/$NB_USER
RUN rm -r /home/$NB_USER/Source-test_docker

ENV DEBUG=false \
    GALAXY_WEB_PORT=10000 \
    NOTEBOOK_PASSWORD=none \
    CORS_ORIGIN=none \
    DOCKER_PORT=none \
    API_KEY=none \
    HISTORY_ID=none \
    REMOTE_HOST=none \
    GALAXY_URL=none

RUN chown -R $NB_USER /home/$NB_USER /import

USER ${NB_USER}

WORKDIR /import

CMD /startup.sh
