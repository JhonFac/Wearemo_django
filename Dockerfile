FROM python:3.10.14-alpine

RUN pip install --upgrade pip

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache mysql-client mysql-dev jpeg-dev mariadb-dev gcc
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers musl-dev zlib zlib-dev 
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir /code
WORKDIR /code
COPY . /code/

COPY ./scripts /scripts/
RUN chmod +x /scripts/*
RUN apk add --no-cache dos2unix
RUN dos2unix /scripts/entrypoint.sh

CMD ["sh", "/scripts/entrypoint.sh"]
