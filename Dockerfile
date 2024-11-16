# Use a base image with Python
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

# Copy all app files to the container
COPY . /app/

# Expose the Streamlit default port
EXPOSE 8502

# Make the script executable
RUN chmod +x start_app.sh

# Define the default command to start the app
CMD ["/bin/sh", "./start_app.sh"]