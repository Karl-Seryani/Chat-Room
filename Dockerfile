# Use Python 3.9 as the base image
FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Copy the chatroom files into the container
COPY chatroom.py .
COPY server.py .

# Expose the port that the server will use
EXPOSE 12345

# Run the server when the container starts
CMD ["python", "server.py"]
