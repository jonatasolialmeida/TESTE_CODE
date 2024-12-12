# backend/Dockerfile
FROM python:3.12.7-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "codeleap_network.wsgi:application", "-b", "0.0.0.0:8000"]