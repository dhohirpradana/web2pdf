FROM python:3.8-slim-buster

# Install necessary dependencies
RUN apt-get update \
    && apt-get install -y \
        wget \
        gnupg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y \
        google-chrome-stable \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set up the working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . /app

# Expose the port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
# Set DISPLAY environment variable
ENV DISPLAY=:99

# Uncomment the following lines if you have SSL certificate and key files
# COPY cert.pem /app
# COPY key.pem /app

# Run the Flask application
CMD ["sh", "-c", "echo Halo"]
