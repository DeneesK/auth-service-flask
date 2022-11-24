FROM python:3.10
WORKDIR /opt/app

RUN pip install -r requirements.txt

COPY api api
COPY core core
COPY db db
COPY models models
COPY services services
