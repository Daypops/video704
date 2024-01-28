# api/Dockerfile
FROM python:3.10-alpine

WORKDIR /app

ENV FLASK_RUN_PORT=5000

EXPOSE 5000

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD flask --app . run --host 0.0.0.0 --debug
