# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY posterpal.py /usr/src/app
COPY requirements.txt /usr/src/app

# Install build dependencies for Pillow and general setup
RUN apt-get update && apt-get install -y \
    gcc \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir /data/assets
RUN mkdir /data/backup
RUN mkdir /data/processing

# Environment variables with default values
ENV PROCESS=/data/processing \
    BACKUP=/data/backup \
    SHOWS=/data/shows \
    MOVIES=/data/movies \
    ASSETS=/data/assets \
    PMM_ASSETS=false \
    CREATE_BACKUP=true

# Make log directory
RUN mkdir -p /var/log/posterpal

# Volumes for external data
# VOLUME ["/data"]

# Run posterpal.py when the container launches
CMD ["python", "./posterpal.py"]
