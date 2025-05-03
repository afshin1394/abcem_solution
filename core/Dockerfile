FROM python:3.12
# Set the working directory inside the container
WORKDIR /app
# Install PostgreSQL client so pg_isready is available
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Ensure Python finds `customers` as a package
ENV PYTHONPATH=/app
# Copy requirements and install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . /app

## Expose the port (if needed)
# Copy the entrypoint script and make it executable
COPY entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

# Expose the port
EXPOSE 8001

# Use the entrypoint script as the container's entrypoint
#ENTRYPOINT ["/app/entrypoint.sh"]
#CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8001"]


