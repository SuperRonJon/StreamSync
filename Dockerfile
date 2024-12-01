FROM python:3.11

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

ENV PORT=8080
ENV CLIENT_ID=""
ENV OAUTH_TOKEN=""

EXPOSE 8080

CMD ["python", "app.py"]