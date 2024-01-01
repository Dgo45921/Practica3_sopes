# Use the official MySQL image from Docker Hub
FROM mysql:latest

ENV MYSQL_ROOT_PASSWORD=root

# Copy SQL script to initialize the database and user
COPY init.sql /docker-entrypoint-initdb.d/
