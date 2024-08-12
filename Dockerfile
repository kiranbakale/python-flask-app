# Use an official Python runtime as a parent image
FROM python:3.8-alpine

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install dependencies
COPY requirements.txt /app/requirements.txt

WORKDIR /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app



# Set entrypoint to run the Flask application
ENTRYPOINT [ "python" ]

# Run the app
CMD ["new.py"]
