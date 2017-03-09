FROM tiangolo/uwsgi-nginx-flask:flask-python3.5
MAINTAINER Javier Martinez "javyermartinez@gmail.com"

# Set where are we working from, note that from this point onward most '.' will be replaceable with /app
WORKDIR /app

# Copy app and apps config files
COPY ./WhatAClass ./WhatAClass
COPY ./WhatAClass/static ./static
COPY ./config ./config
# Dependencies
COPY requirements-prod.txt .
COPY setup.py .
# Web Server Gateway Interface with uWSGI
COPY wsgi.py .
COPY uwsgi.ini .
# Database initialization script
COPY create_db.py .
# Make sure everything is accesible
ENV PYTHONPATH "$PYTHONPATH:/WhatAClass:/WhatAClass/WhatAClass"

RUN pip3 install --editable .
