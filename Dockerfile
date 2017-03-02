FROM tiangolo/uwsgi-nginx-flask:flask-python3.5
MAINTAINER Javier Martinez "javyermartinez@gmail.com"

# Copy app and apps config files
COPY ./WhatAClass /app/WhatAClass
COPY ./config /app/config
COPY requirements-prod.txt /app
COPY setup.py /app
COPY wsgi.py /app
COPY uwsgi.ini /app
COPY ./WhatAClass/static /app/static

ENV PYTHONPATH "$PYTHONPATH:/WhatAClass:/WhatAClass/WhatAClass"

WORKDIR /app

RUN pip install --editable .
