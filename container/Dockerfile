# syntax=docker/dockerfile:1

FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ["base.py", "settings.ini", "notification_telegram.py", "scheduler.py", "run.sh","./"]

RUN chmod a+x run.sh

CMD ["./run.sh"]
