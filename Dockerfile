FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN pip install flask docker

COPY app.py .
COPY templates/ templates/

EXPOSE 5000

CMD ["python", "app.py"]