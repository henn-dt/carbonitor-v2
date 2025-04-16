#!/bin/sh

# Default values
NGINX_PORT=${NGINX_PORT:-8100}
NGINX_HOST=${NGINX_HOST:-localhost}
FRONTEND_PORT=${FRONTEND_PORT:-8080}
BACKEND_PORT=${BACKEND_PORT:-5000}
FRONTEND_BASE_URL=${FRONTEND_BASE_URL:-"/"}

# Debug prints
echo "Using configuration:"
echo "NGINX_PORT: $NGINX_PORT"
echo "NGINX_HOST: $NGINX_HOST"
echo "FRONTEND_PORT: $FRONTEND_PORT"
echo "FRONTEND_BASE_URL: $FRONTEND_BASE_URL"
echo "BACKEND_PORT: $BACKEND_PORT"


# SSL configuration
if [ -n "$SSL_CERT_PATH" ] && [ -n "$SSL_KEY_PATH" ]; then
    SSL_CONFIG="listen ${NGINX_SSL_PORT:-443} ssl;
                ssl_certificate ${SSL_CERT_PATH};
                ssl_certificate_key ${SSL_KEY_PATH};"
else
    SSL_CONFIG=""
fi

# Replace environment variables in template

export NGINX_PORT
export NGINX_HOST
export FRONTEND_PORT
export FRONTEND_BASE_URL
export BACKEND_PORT
export SSL_CONFIG

envsubst '\$NGINX_PORT \$FRONTEND_BASE_URL \$NGINX_HOST \$FRONTEND_PORT \$BACKEND_PORT \$SSL_CONFIG' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

echo "Generated nginx.conf (start marker)"
echo "----------------------------------------"
cat /etc/nginx/nginx.conf
echo "----------------------------------------"
echo "Generated nginx.conf (end marker)"

# Test the nginx configuration
nginx -t

# Start nginx
exec nginx -g 'daemon off;'
