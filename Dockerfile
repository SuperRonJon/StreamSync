FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY src/ .

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8080", "app:app"]