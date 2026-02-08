FROM nginx:alpine

# Copy static files from public/
COPY public/index.html /usr/share/nginx/html/
COPY public/style.css /usr/share/nginx/html/

# Copy app.js from src/
COPY src/app.js /usr/share/nginx/html/

# Copy nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]