FROM python:slim

WORKDIR /app

RUN pip3 install pika redis[hiredis]

COPY . /app

ENTRYPOINT ["python3"]

CMD ["app.py"]