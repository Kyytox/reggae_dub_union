FROM node:current-alpine3.22

# Set the working directory
WORKDIR /app

# Copy the package.json and package-lock.json files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the application
RUN npm run build

# Set Nginx to serve the built application
# Uncomment the following lines if you want to use Nginx to serve the built files
FROM nginx:alpine
COPY --from=0 /app/dist /usr/share/nginx/html

# Expose the port the app runs on
EXPOSE 80

# Command to run the application
# CMD ["npm", "run", "dev", "--", "--host=0.0.0.0"]

# Use the following command if using Nginx
CMD ["nginx", "-g", "daemon off;"]
