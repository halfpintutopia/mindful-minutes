# Use an official Python runtime as the base image
FROM python:3.10.6

# Set the working directory in the container
WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update \
    && apt-get -y install gcc postgresql \
    && apt-get clean

# Copy the requirements file to the working directory and install the project dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
COPY ./requirements-dev.txt /usr/src/app/requirements-dev.txt
RUN pip install -r requirements-dev.txt

# Copy entrypoint and update permissions
COPY ./scripts/entrypoint.sh /usr/src/app/scripts/entrypoint.sh
RUN chmod +x /usr/src/app/scripts/entrypoint.sh

# Copy the entire project directory to the working directory
COPY . .

# Run entrypoint.sh
ENTRYPOINT ["/usr/src/app/scripts/entrypoint.sh"]