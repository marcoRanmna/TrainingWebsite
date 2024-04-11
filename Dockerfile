FROM python:alpine

# Install system dependencies required for Python packages
RUN apk add --no-cache mariadb-dev build-base

# Additional dependencies for building psutil
RUN apk add --no-cache gcc musl-dev linux-headers

# Set working directory
WORKDIR /InlämningsUppgift16veckkurs

# Copy requirements file
COPY requirements.txt requirements.txt

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Run unittests
RUN python3 unittests.py

# Expose port 5000
EXPOSE 5000

# Run the Flask application
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]