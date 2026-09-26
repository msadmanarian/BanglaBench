# BanglaFactBench Production Container
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency specifications
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy repository code and data
COPY . .

# Expose Web Dashboard Port
EXPOSE 8080

# Default command: launch interactive web dashboard
CMD ["python", "app.py"]
