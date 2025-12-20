FROM python:3.14-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Configure RabbitMQ to log to stdout (avoiding file permission/FS issues)
ENV RABBITMQ_LOGS=-
ENV RABBITMQ_SASL_LOGS=-

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    netcat-openbsd \
    rabbitmq-server \
    redis-server \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY pyproject.toml uv.lock  ./
RUN pip install uv && uv pip install --system .

# Copy project
COPY . .



# Expose port
EXPOSE 8000

# Default command (run the start script)
CMD ["./start.sh"]
