FROM python:3.7-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/code

WORKDIR /code

USER root

RUN apt update && apt install -y netcat

COPY requirements.txt ./

RUN pip3 install -r requirements.txt

COPY . ./

RUN chmod +x entrypoint.sh

# CMD python3 server.py
ENTRYPOINT ["./entrypoint.sh"]
