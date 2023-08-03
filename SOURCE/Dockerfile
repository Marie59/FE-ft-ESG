# Jupyter container used for Galaxy IPython (+other kernels) Integration

# from 5th March 2021
FROM jupyter/datascience-notebook:python-3.10

MAINTAINER Björn A. Grüning, bjoern.gruening@gmail.com

ENV DEBIAN_FRONTEND noninteractive
USER root

RUN apt-get update
RUN apt-get install -y libnetcdf-dev netcdf-bin unzip
RUN apt-get install -y ca-certificates curl libnlopt0 make gcc 
RUN apt-get install -y emacs-nox git g++

# Set channels to (defaults) > bioconda > conda-forge
RUN conda config --add channels conda-forge && \
    conda config --add channels bioconda
    #conda config --add channels defaults
RUN pip install --upgrade pip
RUN pip install --no-cache-dir bioblend galaxy-ie-helpers

ENV JUPYTER /opt/conda/bin/jupyter
ENV PYTHON /opt/conda/bin/python
ENV LD_LIBRARY_PATH /opt/conda/lib/

# Python packages
RUN conda config --add channels conda-forge && \
    conda config --add channels bioconda && \
    conda install --yes --quiet \
    biopython \
    rpy2 \
    bash_kernel \
    #octave_kernel \
    # Scala
    #spylon-kernel \
    # Java
    #scijava-jupyter-kernel \
    # ansible
    ansible-kernel \
    bioblend galaxy-ie-helpers \
    # Jupyter widgets
    jupytext \
    cython patsy statsmodels cloudpickle dill r-xml && conda clean -yt && \
    pip install jupyterlab_hdf
    
RUN conda install -c conda-forge source
RUN conda install -c conda-forge folium
RUN conda install -c conda-forge ftputil
RUN conda install -c conda-forge matplotlib
RUN conda install -c conda-forge altair
RUN conda install -c conda-forge shapely

ADD ./startup.sh /startup.sh
#ADD ./monitor_traffic.sh /monitor_traffic.sh
ADD ./get_notebook.py /get_notebook.py

# We can get away with just creating this single file and Jupyter will create the rest of the
# profile for us.
RUN mkdir -p /home/$NB_USER/.ipython/profile_default/startup/ && \
    mkdir -p /home/$NB_USER/.jupyter/custom/

COPY ./ipython-profile.py /home/$NB_USER/.ipython/profile_default/startup/00-load.py
COPY jupyter_notebook_config.py /home/$NB_USER/.jupyter/
COPY jupyter_lab_config.py /home/$NB_USER/.jupyter/

ADD ./custom.js /home/$NB_USER/.jupyter/custom/custom.js
ADD ./custom.css /home/$NB_USER/.jupyter/custom/custom.css
ADD ./default_notebook.ipynb /home/$NB_USER/notebook.ipynb

# Download notebooks
RUN cd   /home/$NB_USER/;  \
    wget -O Source-main.zip https://github.com/fair-ease/Source/archive/refs/heads/main.zip; unzip Source-main.zip; \
    rm /home/$NB_USER/Source-main.zip

RUN mv /home/$NB_USER/Source-main/notebooks /home/$NB_USER
RUN rm -r /home/$NB_USER/Source-main

# ENV variables to replace conf file
ENV DEBUG=false \
    GALAXY_WEB_PORT=10000 \
    NOTEBOOK_PASSWORD=none \
    CORS_ORIGIN=none \
    DOCKER_PORT=none \
    API_KEY=none \
    HISTORY_ID=none \
    REMOTE_HOST=none \
    GALAXY_URL=none

# @jupyterlab/google-drive  not yet supported

USER root

RUN apt-get -qq update && \
    apt-get install -y net-tools procps && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# /import will be the universal mount-point for Jupyter
# The Galaxy instance can copy in data that needs to be present to the Jupyter webserver
RUN mkdir -p /import/jupyter/outputs/ && \
    mkdir -p /import/jupyter/data && \
    mkdir /export/ && \
    chown -R $NB_USER:users /home/$NB_USER/ /import /export/

##USER jovyan

WORKDIR /import

# Start Jupyter Notebook
CMD /startup.sh

