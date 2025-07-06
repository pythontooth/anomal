#!/bin/bash

CONTAINER_NAME="anonmal_temp"
IMAGE_NAME="ubuntu:latest"

if ! docker image inspect $IMAGE_NAME > /dev/null 2>&1; then
    echo "Downloading Ubuntu image (one-time download)..."
    docker pull $IMAGE_NAME
fi

docker rm -f $CONTAINER_NAME 2>/dev/null

docker run --rm -it \
  --name $CONTAINER_NAME \
  --hostname anonmal \
  --tmpfs /tmp \
  --tmpfs /home/anon \
  -e HISTFILE=/dev/null \
  $IMAGE_NAME \
  bash --norc --noprofile