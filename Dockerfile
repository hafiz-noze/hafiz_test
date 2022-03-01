FROM python:3.8-alpine

RUN pip install pika

RUN pip install flask

COPY . .

ENTRYPOINT [ "python"]

CMD ["app.py"]