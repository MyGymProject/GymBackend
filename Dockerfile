# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies needed for psycopg2, bcrypt, etc.
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the same port you will run uvicorn on
EXPOSE 8000

# Run FastAPI app with uvicorn
# Replace `main:app` with your actual module and app instance
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
