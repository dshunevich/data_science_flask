FROM python:3.9.4-buster

COPY . /root

WORKDIR /root

RUN pip install flask gunicorn numpy sklearn joblib flask_wtf pandas