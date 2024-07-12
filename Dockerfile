# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy the requirements file into the working directory
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the code into the working directory
COPY . /app/

# Expose the port Flask runs on
EXPOSE 5000

# Define the command to run the Flask application
CMD ["flask", "run", "--host=0.0.0.0"]