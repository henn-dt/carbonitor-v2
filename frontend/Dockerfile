# Build frontend
FROM node:20-alpine

# Initialize args
ARG BUILD_HASH=dev-build
ARG UID=0
ARG GID=0
ARG CACHEBUST=1

# Set working directory
WORKDIR /frontend

# Install system dependencies
# Copy package files first for better caching
COPY ./package.json ./package-lock.json* ./
RUN npm install

# Explicitly install speckle viewer (with --force to ensure installation)
RUN npm install @speckle/viewer --force

# Copy frontend code
COPY --chown=$UID:$GID . .

RUN chmod +x /frontend/docker-entrypoint.sh

# Set the entrypoint script
ENTRYPOINT ["/bin/sh", "/frontend/docker-entrypoint.sh"]