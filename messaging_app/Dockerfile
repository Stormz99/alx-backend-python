# Dockerfile (development)
FROM python:3.10-slim-bullseye

# Prevent .pyc files and enable unbuffered output (helps with logs)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies needed for building some packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies (done as root)
COPY requirements.txt /app/
RUN python -m pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Create a non-root user and give it ownership of the app directory
# --create-home creates /home/app in case some libs expect a home dir
RUN useradd --create-home --shell /bin/false app && \
    mkdir -p /app && chown -R app:app /app

# Copy app code and set ownership in one step (supported by modern Docker)
COPY --chown=app:app . /app

# Switch to the non-root user
USER app

EXPOSE 8000

# NOTE: Django's runserver is for development only
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
