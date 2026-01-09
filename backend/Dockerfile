# Use official Python slim image (matches your runtime.txt: 3.12)
FROM python:3.12-slim

# Set workdir
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install deps with pip (no mise/UV involved)
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose port (Railway uses $PORT)
EXPOSE 8000

# Run with uvicorn (matches your code)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]