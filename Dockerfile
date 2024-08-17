# Use the official Python image as the base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy the poetry.lock and pyproject.toml files
COPY poetry.lock pyproject.toml ./

# Install dependencies
RUN poetry install --no-dev --no-root

# Copy the application code into the container
COPY . .

# Make the installation script executable
RUN chmod +x install_tree_sitter_languages.sh

# Run the Tree-sitter language installation script
RUN ./install_tree_sitter_languages.sh

# Expose the port on which the application will run
EXPOSE 8000

# Set the command to run the FastAPI application
CMD ["poetry", "run", "uvicorn", "github_app.main:app", "--host", "0.0.0.0", "--port", "8000"]