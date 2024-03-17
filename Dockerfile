FROM python:3.10-slim-bullseye
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip \
    -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]