# Use official NGINX image from Docker Hub
FROM nginx:latest

# Copy custom HTML file into NGINX container
COPY html /usr/share/nginx/html

# Expose the default NGINX port
EXPOSE 80

# Start NGINX in the foreground
CMD ["nginx", "-g", "daemon off;"]

