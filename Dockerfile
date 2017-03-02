FROM tiangolo/uwsgi-nginx-flask:flask-python3.5
MAINTAINER Javier Martinez "javyermartinez@gmail.com"

# Copy app and apps config files
COPY ./WhatAClass /WhatAClass/WhatAClass
COPY ./config /WhatAClass/config
COPY ./requirements-prod.txt /WhatAClass
COPY ./setup.py /WhatAClass
COPY uwsgi.ini /app

ENV PYTHONPATH "$PYTHONPATH:/WhatAClass:/WhatAClass/WhatAClass"

WORKDIR /WhatAClass

RUN pip install --editable .
