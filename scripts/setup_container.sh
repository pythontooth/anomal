#!/bin/bash

SETTINGS_FILE="$(dirname "$0")/../settings/container-settings.json"

get_json_value() {
  python3 -c "import sys, json; print(json.load(open(sys.argv[1]))[sys.argv[2]])" "$1" "$2"
}

CONTAINER_NAME=$(get_json_value "$SETTINGS_FILE" container_name)
IMAGE_NAME=$(get_json_value "$SETTINGS_FILE" image_name)
HOSTNAME=$(get_json_value "$SETTINGS_FILE" hostname)
AUTO_REMOVE=$(get_json_value "$SETTINGS_FILE" auto_remove)
NETWORK_MODE=$(get_json_value "$SETTINGS_FILE" network_mode)
CPU_LIMIT=$(get_json_value "$SETTINGS_FILE" cpu_limit)
MEMORY_LIMIT=$(get_json_value "$SETTINGS_FILE" memory_limit)

# Get tmpfs mounts
TMPFS_MOUNTS=$(python3 -c "import sys, json; print(' '.join(['--tmpfs '+m for m in json.load(open(sys.argv[1]))['tmpfs_mounts']]))" "$SETTINGS_FILE")
# Get environment variables
ENV_VARS=$(python3 -c "import sys, json; print(' '.join(['-e '+k+'='+v for k,v in json.load(open(sys.argv[1]))['environment'].items()]))" "$SETTINGS_FILE")

if ! docker image inspect $IMAGE_NAME > /dev/null 2>&1; then
    echo "Downloading Ubuntu image (one-time download)..."
    docker pull $IMAGE_NAME
fi

docker rm -f $CONTAINER_NAME 2>/dev/null

RUN_OPTS="--name $CONTAINER_NAME --hostname $HOSTNAME $TMPFS_MOUNTS $ENV_VARS --network $NETWORK_MODE --cpus $CPU_LIMIT --memory $MEMORY_LIMIT"
if [ "$AUTO_REMOVE" = "true" ]; then
  RUN_OPTS="--rm $RUN_OPTS"
fi

# Install default packages if any
DEFAULT_PACKAGES=$(python3 -c "import sys, json; print(' '.join(json.load(open(sys.argv[1]))['default_packages']))" "$SETTINGS_FILE")

docker run $RUN_OPTS -it $IMAGE_NAME bash -c "apt-get update && apt-get install -y $DEFAULT_PACKAGES; exec bash --norc --noprofile"