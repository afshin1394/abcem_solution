# Use a stable Python version (3.10 recommended)
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

ENV PYTHONPATH=/app
# Ensure Python finds the application package
ENV PYTHONUNBUFFERED=1

# Install system dependencies (for distutils in Python 3.12+)
RUN apt-get update && apt-get install -y python3-distutils && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install setuptools early to avoid distutils issues
RUN pip install --no-cache-dir --upgrade pip setuptools

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Ensure `uvicorn` is installed (in case it's missing from requirements.txt)
RUN pip install --no-cache-dir uvicorn

## Expose the application port
EXPOSE 8000 5678

# Run the application using Uvicorn
CMD ["python3", "-m", "debugpy", "--listen", "0.0.0.0:5678", "-m", "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

