#!/bin/sh

# Reference: https://testdriven.io/courses/tdd-django/continuous-delivery/

: '
Script responsible for updating the Docker image of the Heroku app with the latest image build during the
deployment process. It uses the Heroku API to update the formation of the app, specifically the web process,
with the new Docker image ID. This allows the app to use the updated Docker image for running the web dyno.
'

# Get the Docker Image ID - `--format` option extracts only the image ID
IMAGE_ID=$(docker inspect ${HEROKU_REGISTRY_IMAGE} --format={{.Id}})
# Construct a JSON payload, the payload is in the format expected by the Heroku API to update the app's formation
PAYLOAD='{"updates": [{"type": "web", "docker_image": "'"$IMAGE_ID"'"}]}'

: '
Use `cURL`  to make a PATCH request to the Heroku API with the constructed JSON payload.
The PATCH request is made to update the formation of th app with the new Docker image
'
curl -n -X PATCH https://api.heroku.com/apps/$HEROKU_APP_NAME/formation \
  -d "${PAYLOAD}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/vnd.heroku+json; version=3.docker-releases" \
  -H "Authorization: Bearer ${HEROKU_AUTH_TOKEN}"
