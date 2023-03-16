# Use the official lightweight Python image as the base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install the required system packages, including libmagic, Chromium, and required dependencies for ChromeDriver
RUN apt-get update && \
    apt-get install -y --no-install-recommends libmagic1 wget unzip gnupg ca-certificates chromium && \
    CHROME_VERSION=$(chromium --version | awk '{print $2}' | cut -d'.' -f1) && \
    wget -q https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION} -O - | xargs -I {} wget -q https://chromedriver.storage.googleapis.com/{}/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf /var/lib/apt/lists/* && \
    rm -f chromedriver_linux64.zip

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 8080

# Start the application
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--threads", "8", "main:app"]
