# Use python runtime as a parent image
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    ca-certificates \
    chromium \
    && rm -rf /var/lib/apt/lists/*

# Install Nodejs and npm
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g npm@latest

# Set the working directory in the container
WORKDIR /code

# Copy the dependencies files to the container
COPY ./requirements.txt ./
COPY ./package.json ./
COPY ./package-lock.json ./

# Install the Python runtime dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Nodejs dependencies
RUN npm ci

# Copy the current working directory contents into the container at /code
COPY . /code

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Run streamlit when the container launches
CMD ["streamlit", "run", "Dashboard.py"]
