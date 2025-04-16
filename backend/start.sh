#!/bin/bash

# set environmental variables
export FRONTEND_PORT=${FRONTEND_PORT:-8080}
export BACKEND_PORT=${BACKEND_PORT:-5000}

# Function to extract host and port from DATABASE_URL
parse_db_url() {
    # Extract host and port from DATABASE_URL
    if [[ $EXTERNAL_DATABASE_URL =~ @([^/:]+)(:([0-9]+))?/ ]]; then
        DB_HOST=${BASH_REMATCH[1]}
        DB_PORT=${BASH_REMATCH[3]}
    else
        echo "Invalid DATABASE_URL format"
        exit 1
    fi

    # Default port if not specified based on database type
    if [[ -z "$DB_PORT" ]]; then
        if [[ $EXTERNAL_DATABASE_URL =~ mysql ]]; then
            DB_PORT=3306
        elif [[ $EXTERNAL_DATABASE_URL =~ postgres ]]; then
            DB_PORT=5432
        elif [[ $EXTERNAL_DATABASE_URL =~ sqlite ]]; then
            DB_PORT=""
        else
            echo "Unsupported database type in DATABASE_URL"
            exit 1
        fi
    fi
}

# Check if using external database
if [ "$USE_EXTERNAL_DB" = "true" ]; then
    echo "Using external database..."
    parse_db_url
    DB_HOST_TO_CHECK=$DB_HOST
    DB_PORT_TO_CHECK=${DB_PORT:-3306}  # Default to 3306 if no port is specified

    # Wait for database to be ready
    echo "Waiting for database at $DB_HOST_TO_CHECK $DB_PORT_TO_CHECK to be ready..."
    while ! nc -z $DB_HOST_TO_CHECK $DB_PORT_TO_CHECK; do
        sleep 1
    done
    echo "Database is ready!"

else
    echo "Using local sqlite db..."
    DB_HOST_TO_CHECK="db"
fi


# Debug info
echo "Current directory: $(pwd)"
echo "Directory contents:"
ls -la
echo "Python path: $PYTHONPATH"



# Start the application
export FLASK_APP=app.main
cd /backend  # Ensure we're in the right directory
echo "Backend will run on port: $BACKEND_PORT"

gunicorn --bind 0.0.0.0:"$BACKEND_PORT" \
         --timeout 180 \
         --log-level debug \
         "app.wsgi:app"



# Keep container running
tail -f /dev/null