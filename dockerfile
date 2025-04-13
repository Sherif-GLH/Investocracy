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

# Create environment variables
ENV AWS_ACCESS_KEY_ID='AKIAYS2NWNIK5KRTHETA'
ENV AWS_SECRET_ACCESS_KEY='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'
ENV AWS_STORAGE_BUCKET_NAME='machine-genius-video'
ENV AWS_S3_SIGNATURE_NAME='s3v4'
ENV AWS_S3_REGION_NAME='us-east-1'
ENV DJANGO_SECRET_KEY='django-insecure-vv)l8iko_0naxkfnkhc+$-_q+z1@i_(+xo_u)m!e)jy7*n9t2y'

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose the application port
EXPOSE 80

# Default command to run the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]
