FROM python:3.9-slim

WORKDIR /app

ENV OUTPUT_DIR=/app/output

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY model.py .
COPY mission15_train.csv .
COPY mission15_test.csv .


CMD ["python", "model.py"]