# Use an official Python runtime as a base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy only requirements.txt to leverage caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Expose the Streamlit port
EXPOSE 8502

# Command to run the app using the shell script
CMD ["sh", "./start_app.sh"]
