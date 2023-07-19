# Use an official Python runtime as the base image
FROM python:3.10.6

# Set the working directory in the container
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update \
    && apt-get -y install gcc postgresql \
    && apt-get clean

RUN pip install --upgrade pip
# Copy the requirements file to the workind directory
COPY ./requirements.txt .

# Install the project dependencies
RUN pip install -r requirements.txt

# Copy entrypoint and update permissions
COPY ./scripts/entrypoint.sh /usr/src/app/scripts/entrypoint.sh
RUN chmod +x /usr/src/app/scripts/entrypoint.sh

# Copy the entire project directory to the working directory
COPY . .

# Expose the port that Django runs on default 8000
#EXPOSE 8000

# Copy the script files to the working directory
#COPY run.sh .
#COPY migrate.sh .
#COPY clear_cache.sh .

# Grant execution permissions to the script files
#RUN chmod +x run.sh migrate.sh clear_cache.sh

# Start the Django development server
#CMD ["gunicorn", "app.mindfulminutes.wsgi:application", "--bind", "0.0.0.0:8000"]

ENTRYPOINT ["/usr/src/app/scripts/entrypoint.sh"]