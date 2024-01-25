##########################
#           STAC          #
##########################
# build stage
FROM node:lts-buster-slim as build-stac

# install git
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y git

#clone repository
RUN git clone https://github.com/radiantearth/stac-browser.git

# move to folder
WORKDIR /stac-browser

# install
RUN npm install

# start application
RUN npm run build -- --catalogUrl=http://localhost:5000

##########################
#        BROWSER          #
##########################
FROM python:3.9-slim

# start from root
WORKDIR /eodag

ENV \
    # force stdin, stdout and stderr to be totally unbuffered. (equivalent to `python -u`)
    PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files(equivalent to `python -B`)
    PYTHONDONTWRITEBYTECODE=1 \
    # enable hash randomization (equivalent to `python -R`)
    PYTHONHASHSEED=random \
    # fault handler (equivalent to `python -X`)
    PYTHONFAULTHANDLER=1 \
    # python encoding
    PYTHONIOENCODING=UTF-8 \
    \
    # set pip settings
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # set time.zone
    TZ=UTC

# update system
RUN apt-get update \
    && apt-get upgrade -y

# reconfigure timezone
RUN echo $TZ > /etc/timezone && \
    apt-get install -y tzdata && \
    rm /etc/localtime && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    apt-get clean

# install locales
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y locales

# ensure locales are configured correctly
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=en_US.UTF-8

ENV LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8

# copy necessary files
COPY setup.cfg setup.cfg
COPY pyproject.toml pyproject.toml
COPY README.rst README.rst
COPY ./eodag /eodag/eodag

# install eodag
RUN python -m pip install .

# add python path
ENV PYTHONPATH="${PYTHONPATH}:/eodag/eodag/resources"


# add user
RUN addgroup --system user \
    && adduser --system --home /home/user --group user

# Install Nginx
RUN apt-get -y update && apt-get -y install nginx

# Copy the Nginx config
COPY ./docker/nginx.conf /etc/nginx/sites-available/default

# Expose the port for access
#EXPOSE 80/tcp

# copie de l'application web
COPY --from=build-stac /stac-browser/dist /usr/share/nginx/html

# copy start-stac script
COPY ./docker/run-stac-server-browser.sh /eodag/run-stac-server.sh

# and make executable
RUN chmod +x /eodag/run-stac-server.sh

# switch to non-root user
#USER user

# Ecrire un nouveau fichier SH pour exécuter STAC et Browser
CMD ["/usr/sbin/nginx", "-g", "daemon off;"]
#ENTRYPOINT ["/eodag/run-stac-server.sh"]
