FROM python:3.9

ENV PYTHONUNBUFFERED=1

RUN mkdir /quera
WORKDIR /quera

RUN pip install --upgrade pip
COPY requirements.txt /quera/
RUN pip install -r requirements.txt

COPY . /quera/