FROM tiangolo/uwsgi-nginx-flask:flask-python3.5
MAINTAINER Javier Martinez "javyermartinez@gmail.com"

# Set where are we working from, note that from this point onward most '.' will be replaceable with /app
WORKDIR /app

# Dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# ssh config
RUN mkdir -p ~/.ssh
COPY resources/id_rsa .
RUN cp id_rsa ~/.ssh/id_rsa && cp id_rsa ~/.ssh/known_hosts && rm id_rsa

# Web Server Gateway Interface with uWSGI
COPY wsgi.py .
COPY uwsgi.ini .

# Directory for file uploads
RUN mkdir -p /images

# nginx configuration for larger file sizes
COPY nginx-conf/nginx.conf /etc/nginx/
COPY nginx-conf/upload.conf /etc/nginx/conf.d/


# Database initialization script
COPY create_db.py .
# Make sure everything is accesible
ENV PYTHONPATH "$PYTHONPATH:/WhatAClass:/WhatAClass/WhatAClass"


# Copy app and apps config files
RUN mkdir -p ./static/images
COPY ./WhatAClass/static ./static
COPY ./config ./config
COPY ./WhatAClass ./WhatAClass


