FROM ubuntu:latest

# Install Python
RUN apt-get update && apt-get install -y python3

# Set the working directory
WORKDIR /tmp