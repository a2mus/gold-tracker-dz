FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for PaddleOCR
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/

# Create sessions directory
RUN mkdir -p /app/sessions

CMD ["python", "-m", "src.scraper"]
