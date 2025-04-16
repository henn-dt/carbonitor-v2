# Build main container
FROM nginx:alpine

# Install envsubst
RUN apk add --no-cache gettext \
    && apk add --no-cache dos2unix

# Copy template and entrypoint script
COPY nginx.conf.template /etc/nginx/nginx.conf.template
COPY docker-entrypoint.sh /docker-entrypoint.sh

# verify line endings in template file
RUN dos2unix /etc/nginx/nginx.conf.template

# Make entrypoint script executable
RUN chmod +x /docker-entrypoint.sh

# Set entrypoint
ENTRYPOINT ["/docker-entrypoint.sh"]



# This creates a folder for the Frontend dist
RUN mkdir -p /usr/share/nginx/html/carbonitor  
#COPY nginx.conf /etc/nginx/conf.d/default.conf