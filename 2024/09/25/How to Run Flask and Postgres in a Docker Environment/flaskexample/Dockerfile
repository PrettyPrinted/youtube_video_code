FROM python:3.12

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

# CMD ["flask", "run", "-h", "0.0.0.0"]