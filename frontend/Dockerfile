# Stage 1: Build the React application
FROM node:20-alpine AS build

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json to leverage Docker cache
COPY package.json ./
COPY package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the frontend application code
COPY . .

# Build the application
RUN npm run build

# Stage 2: Serve the static files with Nginx
FROM nginx:stable-alpine

# Copy the custom Nginx configuration
# This is important for routing and handling single-page applications correctly
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy the built application from the builder stage to Nginx's web root
COPY --from=build /app/build /usr/share/nginx/html

# Expose the port the app runs on
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]