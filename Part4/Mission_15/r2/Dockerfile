FROM python:3.9-slim

WORKDIR /app

ENV OUTPUT_DIR=/app/output

# requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install jupyter nbconvert

# notebook & data
COPY researcher2.ipynb .

# 실행
CMD ["jupyter", "nbconvert", "--to", "notebook", "--execute","researcher2.ipynb", "--output", "executed_researcher2.ipynb"]