FROM python:3.8-slim

WORKDIR /etl
COPY requirements.txt requirements.txt
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . .
CMD python -m etl
