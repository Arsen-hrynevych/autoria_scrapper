ARG PYTHON_VERSION=3.11.0
FROM python:${PYTHON_VERSION} as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y postgresql-client

WORKDIR /app

# Now you can install poetry
RUN pip install poetry

# Copy poetry related files
COPY pyproject.toml .

# Install poetry dependencies
RUN poetry install --no-root

# Copy the source code into the container.
COPY . .

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD poetry run python main.py
