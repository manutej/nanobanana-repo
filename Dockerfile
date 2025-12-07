# NanoBanana Image Generation Service - Docker Container
# Simple, production-ready container for Cloud Run

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY templates/ ./templates/

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Expose port
EXPOSE 8080

# Run with gunicorn (production-ready WSGI server)
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 src.main:app
