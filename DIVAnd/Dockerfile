# Jupyter container used for Galaxy IPython (+other kernels) Integration

# from 5th March 2021
FROM jupyterhub/singleuser:3.1

MAINTAINER Alexander Barth <a.barth@ulg.ac.be>

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

ENV JUPYTER /opt/conda/bin/jupyter
ENV PYTHON /opt/conda/bin/python
ENV LD_LIBRARY_PATH /opt/conda/lib/

    
RUN conda install -c conda-forge ncurses
RUN conda install -y ipywidgets
RUN conda install -y matplotlib
RUN conda install -c conda-forge jupyterlab-git
RUN conda install -c conda-forge contourpy 

RUN wget -O /usr/share/emacs/site-lisp/julia-mode.el https://raw.githubusercontent.com/JuliaEditorSupport/julia-emacs/master/julia-mode.el

# Install julia
ADD install_julia.sh .
RUN bash install_julia.sh; rm install_julia.sh

# install packages as user (to that the user can temporarily update them if necessary)
# and precompilation

USER jovyan

ENV LD_LIBRARY_PATH=
ENV JULIA_PACKAGES="CSV DataAssim DIVAnd DataStructures FFTW FileIO Glob HTTP IJulia ImageIO Images Interact Interpolations JSON Knet MAT Missings NCDatasets PackageCompiler PhysOcean PyCall PyPlot Roots SpecialFunctions StableRNGs VideoIO"

RUN julia --eval 'using Pkg; Pkg.add(split(ENV["JULIA_PACKAGES"]))'

RUN pip install --upgrade pip
RUN pip install --no-cache-dir bioblend galaxy-ie-helpers
ADD ./get_notebook.py /get_notebook.py

COPY ./ipython-profile.py /home/$NB_USER/.ipython/profile_default/startup/00-load.py


RUN pip install jupyterlab_hdf
    
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
RUN mkdir -p /home/$NB_USER/
RUN cd   /home/$NB_USER/;  \
    wget -O master.zip https://github.com/gher-ulg/Diva-Workshops/archive/master.zip; unzip master.zip; \
    rm /home/$NB_USER/master.zip
 
RUN mv /home/$NB_USER/Diva-Workshops-master/notebooks /home/$NB_USER
RUN rm -r /home/$NB_USER/Diva-Workshops-master

USER jovyan
ADD emacs /home/jovyan/.emacs
RUN mkdir -p /home/jovyan/.julia/config
ADD startup.jl /home/jovyan/.julia/config/startup.jl

RUN julia --eval 'using Pkg; pkg"precompile"'

USER root
# Example Data
RUN mkdir /data
RUN mkdir /data/Diva-Workshops-data
RUN curl https://dox.ulg.ac.be/index.php/s/Px6r7MPlpXAePB2/download | tar -C /data/Diva-Workshops-data -zxf -
RUN ln -s /opt/julia-* /opt/julia

##USER jovyan

RUN julia -e 'using IJulia; IJulia.installkernel("Julia with 4 CPUs",env = Dict("JULIA_NUM_THREADS" => "4"))'


USER root
# Pre-compiled image with PackageCompiler
RUN julia --eval 'using Pkg; pkg"add PackageCompiler"'
ADD DIVAnd_precompile_script.jl .
ADD make_sysimg.sh .
RUN ./make_sysimg.sh
RUN mkdir -p /home/jovyan/.local
RUN mv sysimg_DIVAnd.so DIVAnd_precompile_script.jl make_sysimg.sh  DIVAnd_trace_compile.jl  /home/jovyan/.local
RUN rm -f test.xml Water_body_Salinity.3Danl.nc Water_body_Salinity.4Danl.cdi_import_errors_test.csv Water_body_Salinity.4Danl.nc Water_body_Salinity2.4Danl.nc
RUN julia -e 'using IJulia; IJulia.installkernel("Julia-DIVAnd precompiled", "--sysimage=/home/jovyan/.local/sysimg_DIVAnd.so")'
RUN julia -e 'using IJulia; IJulia.installkernel("Julia-DIVAnd precompiled, 4 CPUs)", "--sysimage=/home/jovyan/.local/sysimg_DIVAnd.so",env = Dict("JULIA_NUM_THREADS" => "4"))'

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
ADD run_galaxy.sh /usr/local/bin/run_galaxy.sh

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

#USER jovyan

COPY ./healthcheck_notebook.sh /bin/healthcheck.sh
HEALTHCHECK --interval=30s --timeout=10s CMD /bin/healthcheck.sh
# issue https://github.com/gher-uliege/DIVAnd-jupyterhub/issues/6
# This should not be necessary anymore for julia 1.9
# We are assuming the python is compiled with a newer libstdc++ than julia
# (otherwise the file should not be removed)
RUN ["/bin/sh","-c","rm /opt/julia-1.8.*/lib/julia/libstdc++.so.*"]

WORKDIR /import

CMD ["bash", "/usr/local/bin/run_galaxy.sh"]

USER root
RUN chmod 777 /home/jovyan/ -R
USER jovyan

