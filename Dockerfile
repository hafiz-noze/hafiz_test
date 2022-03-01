FROM python:3.8-alpine

RUN apk add --no-cache python3-pip

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT [ "python"]

CMD ["app.py"]