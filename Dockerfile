FROM python:3.10-slim AS builder

RUN apt-get update && \
    apt-get install -y zip && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /usr/app

COPY requirements.txt .

RUN pip install -r requirements.txt -t /opt/python

WORKDIR /opt

RUN zip -r9 /usr/app/ai_agents_lambda_layer.zip python
