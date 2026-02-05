# Use a stable Python version
FROM python:3.12-slim

# Install system dependencies for build-time (like git or compilers)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Streamlit uses port 8501 by default
EXPOSE 8501

# Run the application
ENTRYPOINT ["streamlit", "run", "meeting_agent.py", "--server.port=8501", "--server.address=0.0.0.0"]
