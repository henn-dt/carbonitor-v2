#!/bin/sh
set -e

# Default port is 8080 if FRONTEND_PORT is not set
FRONTEND_PORT=${FRONTEND_PORT:-8080}
BACKEND_PORT=${BACKEND_PORT:-5000}
VITE_BASE_PATH=${VITE_BASE_PATH:-"./"}

# Check if ENV is set
if [ -z "$ENV" ]; then
  echo "ENV variable is not set, defaulting to dev mode"
  ENV="dev"
fi

# Run based on environment
if [ "$ENV" = "dev" ]; then
  echo "Starting in development mode on port $FRONTEND_PORT..."
  echo "looking for API on port $BACKEND_PORT"
  export NODE_ENV=development
  export VITE_ALLOW_HOSTS=true
  exec npm run dev -- --host 0.0.0.0 --force
elif [ "$ENV" = "prod" ]; then
  echo "Building production bundle..."
  export NODE_ENV=production
  export VITE_ALLOW_HOSTS=true
  npm run build
  
  echo "Installing serve..."
  npm install -g serve
  
  echo "Starting production server on port $FRONTEND_PORT..."
  exec serve -s dist -l $FRONTEND_PORT
else
  echo "Unknown ENV value: $ENV. Must be 'dev' or 'prod'"
  exit 1
fi