# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set the working directory
WORKDIR /app/backend

# Copy the requirements file first
COPY ./backend/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY ./backend .

# Expose the port the app runs on
EXPOSE 5000

# Define the command to run the app
CMD ["python", "api.py"]