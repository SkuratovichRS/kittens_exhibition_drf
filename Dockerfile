FROM python:3.10

WORKDIR /workdir

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY manage.py manage.py
COPY kitten_exhibition kitten_exhibition
COPY exhibition exhibition

