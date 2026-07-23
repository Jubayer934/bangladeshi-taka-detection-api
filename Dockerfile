# Use the full Python image for maximum compatibility
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000
ENV YOLO_CONFIG_DIR=/tmp

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# 1. Install base requirements
# 2. Force install Headless OpenCV to avoid libGL errors
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir opencv-python-headless

# Copy the entire project
COPY . .

# Expose port 8000
EXPOSE 8000

# Universal command for Local and Cloud
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
