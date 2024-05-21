# Set base image
FROM pytorch/pytorch:2.1.2-cuda12.1-cudnn8-runtime

# Define environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install required packages
RUN apt update && apt install -y \
    curl \
    software-properties-common \
    git

# Set the workingdirectory
WORKDIR /workspace
