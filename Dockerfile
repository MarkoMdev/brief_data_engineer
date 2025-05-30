FROM python:3.11-slim

WORKDIR /usr/src/app

COPY requirements.txt .          
RUN pip install --no-cache-dir -r requirements.txt

COPY scripts/*.py .

CMD ["python", "init_db.py"]
