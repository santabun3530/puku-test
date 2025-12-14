FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .


ARG REACT_APP_API_URL
ARG REACT_APP_RECIPE_SERVICE_URL
ARG REACT_APP_RATING_SERVICE_URL

ENV REACT_APP_API_URL=$REACT_APP_API_URL
ENV REACT_APP_RECIPE_SERVICE_URL=$REACT_APP_RECIPE_SERVICE_URL
ENV REACT_APP_RATING_SERVICE_URL=$REACT_APP_RATING_SERVICE_URL

RUN npm run build

FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]





# FROM node:18-alpine

# WORKDIR /app

# COPY package*.json ./
# RUN npm install
# COPY . .
# RUN npm run build
# RUN npm install -g serve

# EXPOSE 3000
# CMD ["serve", "-s", "build", "-l", "3000"]


# # ---- Build Stage ----
# FROM node:18-alpine AS build-stage

# WORKDIR /app

# COPY package*.json ./
# RUN npm install

# COPY . .
# RUN npm run build

# # ---- Nginx Stage ----
# FROM nginx:alpine

# # Remove default nginx files
# RUN rm -rf /usr/share/nginx/html/*

# # Copy React build output
# COPY --from=build-stage /app/build /usr/share/nginx/html

# EXPOSE 80

# CMD ["nginx", "-g", "daemon off;"]
