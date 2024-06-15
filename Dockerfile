# Use the official Python image as the base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy the poetry.lock and pyproject.toml files
COPY poetry.lock pyproject.toml ./

# Install dependencies
RUN poetry install --no-dev --no-root

# Copy the application code into the container
COPY . .

# Expose the port on which the application will run
EXPOSE 8000

# Set the command to run the FastAPI application
CMD ["poetry", "run", "uvicorn", "github_app.main:app", "--host", "0.0.0.0", "--port", "8000"]