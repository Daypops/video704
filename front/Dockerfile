# front/Dockerfile
FROM python:3.10-alpine

WORKDIR /app

ENV FLASK_RUN_PORT=80

EXPOSE 80/tcp

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD flask --app . init-db && flask --app . run --host 0.0.0.0 --debug
