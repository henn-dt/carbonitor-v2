# Build backend container
FROM python:3.10

# Initialize args
ARG BUILD_HASH=dev-build
ARG UID=0
ARG GID=0
ARG CACHEBUST=1
# This is important for seeing print statements
ENV PYTHONUNBUFFERED=1
# Print cache busting
RUN echo "Cache busting at: $CACHEBUST"

# Set working directory
WORKDIR /backend

# Set environment variables
ENV HOME=/root
ENV PYTHONPATH=/backend
ENV BACKEND_BUILD_VERSION=${BUILD_HASH}
ENV DOCKER=true

# Install system dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
    git \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Setup backend
# Copy requirements first to leverage Docker cache
COPY --chown=$UID:$GID requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt
# COPY .env .env
# Copy application code
COPY --chown=$UID:$GID . .

# Copy and make start script executable
COPY --chown=$UID:$GID start.sh .
RUN chmod +x start.sh

# Command to run the application
CMD ["bash", "start.sh"]