#Base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy the project files to the container
COPY . /app


# Install Python dependencies
RUN pip install -r requirements.txt

# Expose the application port
EXPOSE 80

# Default command to run the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]
