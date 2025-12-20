# StreamSentry: Contextual Suitability Analysis Engine

**StreamSentry** is a distributed system designed to classify video content risks at scale. It leverages a decoupled architecture to perform asynchronous analysis of YouTube channels against GARM (Global Alliance for Responsible Media) suitability frameworks.

## Architecture

The system follows a cloud-native, microservices-ready pattern:

*   **Web Layer (Django 4.2)**: Handles API requests, user dashboard, and task dispatching.
*   **Message Broker (RabbitMQ)**: Ensures reliable task queuing and decoupling of the web and worker layers.
*   **Processing Engine (Celery)**: Performs the "heavy lifting" (metadata fetching, mock inference, and scoring) in the background.
*   **Data Persistence (PostgreSQL 15)**: Stores structured relational data and JSON-based GARM scores.
*   **Caching/Locking (Redis 7)**: Handles task result caching and distributed locks to prevent duplicate processing.

## Key Features

*   **Asynchronous Processing**: Non-blocking analysis workflow using Celery & RabbitMQ.
*   **GARM Compliance**: Granular scoring for Hate Speech, Violence, and Adult content.
*   **Resiliency**: Automated retries and Dead Letter Queues (DLQ) for failed tasks.
*   **Scalable**: Worker nodes can be scaled horizontally independent of the web server.

## Local Development

### Prerequisites
*   Docker & Docker Compose
*   Python 3.11+
*   `uv` (or pip)

### Quick Start

1.  **Start Infrastructure**
    ```bash
    docker-compose up -d
    ```

2.  **Install Dependencies**
    ```bash
    uv sync
    # Or: pip install -r requirements.txt
    ```

3.  **Run Migrations**
    ```bash
    uv run manage.py migrate
    ```

4.  **Start Services**
    *   **Web Server**:
        ```bash
        uv run manage.py runserver
        ```
    *   **Worker Node**:
        ```bash
        celery -A ad_safety_project worker --loglevel=info
        ```

5.  **Access Dashboard**
    Navigate to `http://127.0.0.1:8000`.

## Deployment

This project is configured for PaaS deployment (Railway, Render, Heroku).
*   **Dockerfile** included for containerized builds.
*   **Procfile** included for process management.
*   **Settings**: Fully configurable via environment variables (`DATABASE_URL`, `CELERY_BROKER_URL`, etc.).

---
*Built with Django & Celery.*
