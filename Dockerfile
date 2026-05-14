# Use a lightweight, professional Python base
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Install system-level dependencies if needed
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker's cache
COPY requirements.txt .

# Install libraries without saving cache (saves space)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code and the knowledge base
COPY . .

# Expose Streamlit's default port
EXPOSE 8501

# Start the application
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]