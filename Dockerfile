FROM python:3-alpine

RUN apk add gcc make linux-headers musl-dev && \
    pip install flask Flask-Limiter gunicorn meinheld raven requests && \
    apk del gcc make

EXPOSE 80

CMD gunicorn --bind 0.0.0.0:80 --worker-class="egg:meinheld#gunicorn_worker" --workers 1 proxy:app

COPY proxy.py /