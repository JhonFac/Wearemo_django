FROM python:3.10.14-alpine

RUN pip install --upgrade pip

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /code
WORKDIR /code
COPY . /code/

COPY ./scripts /scripts/
RUN chmod +x /scripts/*
RUN apk add --no-cache dos2unix
RUN dos2unix /scripts/entrypoint.sh

CMD ["sh", "/scripts/entrypoint.sh"]
