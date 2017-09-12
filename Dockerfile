FROM tiangolo/uwsgi-nginx-flask:flask-python3.5
MAINTAINER Javier Martinez "javyermartinez@gmail.com"

# Set where are we working from, note that from this point onward most '.' will be replaceable with /app
WORKDIR /app

# Copy app and apps config files
COPY ./WhatAClass ./WhatAClass
COPY ./WhatAClass/static ./static
RUN mkdir -p ./static/images
COPY ./config ./config
# Dependencies
COPY setup.py .
# Web Server Gateway Interface with uWSGI
COPY wsgi.py .
COPY uwsgi.ini .
# ssh config
RUN mkdir -p ~/.ssh
COPY resources/id_rsa .
RUN cp id_rsa ~/.ssh/id_rsa && cp id_rsa ~/.ssh/known_hosts && rm id_rsa
# Directory for file uploads
RUN mkdir -p /images

# nginx configuration for larger file sizes
COPY nginx.conf /etc/nginx/


# Database initialization script
COPY create_db.py .
# Make sure everything is accesible
ENV PYTHONPATH "$PYTHONPATH:/WhatAClass:/WhatAClass/WhatAClass"

RUN pip3 install --editable .
