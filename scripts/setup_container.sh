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
PIDS_LIMIT=$(get_json_value "$SETTINGS_FILE" pids_limit)

# get 'em to bytes
if [[ "$MEMORY_LIMIT" =~ ^[0-9]+[gG]$ ]]; then
  MEM_BYTES=$(( ${MEMORY_LIMIT%[gG]} * 1024 * 1024 * 1024 ))
elif [[ "$MEMORY_LIMIT" =~ ^[0-9]+[mM]$ ]]; then
  MEM_BYTES=$(( ${MEMORY_LIMIT%[mM]} * 1024 * 1024 ))
else
  MEM_BYTES=$MEMORY_LIMIT
fi

CPU_PERIOD=100000
CPU_QUOTA=$(awk -v c="$CPU_LIMIT" 'BEGIN{printf "%d", c*100000}')

# --- BUBBLEWRAP (bwrap) FULL ISOLATION, prolly but not guaranteed ---
# Requires: bwrap, debootstrap (for Ubuntu rootfs), and root privileges

UBUNTU_ROOTFS="/tmp/anonmal_ubuntu_rootfs"
if [ ! -d "$UBUNTU_ROOTFS" ]; then
  echo "[anonmal] Creating minimal Ubuntu rootfs in $UBUNTU_ROOTFS ..."
  debootstrap --variant=minbase noble "$UBUNTU_ROOTFS" http://archive.ubuntu.com/ubuntu/
fi

# Set up tmpfs mounts
TMPFS_MOUNTS=(/tmp /home/anon /dev/shm /run /var/tmp)
BWRAP_TMPFS_ARGS=()
for mnt in "${TMPFS_MOUNTS[@]}"; do
  BWRAP_TMPFS_ARGS+=(--tmpfs "$mnt")
  mkdir -p "$UBUNTU_ROOTFS$mnt"
done

# Set up environment variables
ENV_VARS=$(python3 -c "import sys, json; env=json.load(open(sys.argv[1]))['environment']; print(' '.join(['--setenv '+k+' '+v for k,v in env.items()]))" "$SETTINGS_FILE")


# --- Set up cgroup v2 for CPU and memory limits ---
CGROUP_ROOT=/sys/fs/cgroup
CGROUP_NAME=anonmal_$$
CGROUP_PATH="$CGROUP_ROOT/$CGROUP_NAME"

# Ensure we can create cgroups and apply limits
if [ -d "$CGROUP_ROOT" ] && [ -w "$CGROUP_ROOT" ]; then
  echo "[anonmal] Setting up resource limits via cgroups..."
  mkdir -p "$CGROUP_PATH" 2>/dev/null || {
    echo "[anonmal] Warning: Could not create cgroup. Running without strict limits."
    CGROUP_PATH=""
  }
  
  if [ -n "$CGROUP_PATH" ]; then
    # Enable controllers
    echo "+memory +cpu +pids" > "$CGROUP_ROOT/cgroup.subtree_control" 2>/dev/null || true
    
    # Set limits
    echo "$MEM_BYTES" > "$CGROUP_PATH/memory.max" 2>/dev/null || echo "[anonmal] Warning: Could not set memory limit"
    echo "$CPU_QUOTA $CPU_PERIOD" > "$CGROUP_PATH/cpu.max" 2>/dev/null || echo "[anonmal] Warning: Could not set CPU limit"
    echo "$PIDS_LIMIT" > "$CGROUP_PATH/pids.max" 2>/dev/null || echo "[anonmal] Warning: Could not set process limit"
    
    # Set up cleanup on exit
    trap "rmdir '$CGROUP_PATH' 2>/dev/null || true" EXIT
  fi
else
  echo "[anonmal] Warning: cgroup v2 not available or not writable. Resource limits may not be enforced!"
  CGROUP_PATH=""
fi

# Create anon user if not present and ensure passwordless su
chroot "$UBUNTU_ROOTFS" bash -c 'id anon 2>/dev/null || useradd -m -s /bin/bash anon'
chroot "$UBUNTU_ROOTFS" passwd -d anon

# Enable universe and multiverse in chroot (robust)
chroot "$UBUNTU_ROOTFS" bash -c "grep -E 'universe|multiverse' /etc/apt/sources.list || \
  sed -i '/^deb .*main/ s/$/ universe multiverse/' /etc/apt/sources.list"
chroot "$UBUNTU_ROOTFS" apt-get update

# Install default packages (ignore missing)
DEFAULT_PACKAGES=$(python3 -c "import sys, json; print(' '.join(json.load(open(sys.argv[1]))['default_packages']))" "$SETTINGS_FILE")
chroot "$UBUNTU_ROOTFS" bash -c "apt-get install -y --no-install-recommends $DEFAULT_PACKAGES || true"

# Set up .bashrc for anon (use a here-doc inside bash -c)
chroot "$UBUNTU_ROOTFS" bash -c 'cat > /home/anon/.bashrc <<EOF
trap "if [ $? -ne 0 ]; then echo \"the system failed, but not yours :) stay safe.\"; fi" ERR
export PS1="anonmal$ "

# Set strict resource limits in bashrc
ulimit -u 64         # Max processes (lower than container setting for safety)
ulimit -f 1048576    # Max file size (1GB in blocks)
ulimit -v 524288     # Max virtual memory (512MB in KB)
ulimit -m 524288     # Max memory size
ulimit -s 8192       # Max stack size
ulimit -t 300        # Max CPU time (5 minutes)

# Display welcome message
echo "🛡️  Welcome to Anonmal isolated environment!"
echo "📊 Resource limits active:"
echo "   Max processes: $(ulimit -u)"
echo "   Max memory: $(ulimit -v) KB"
echo "   Hostname: $(hostname)"
echo ""
echo "💡 Type 'exit' to leave safely or Ctrl+C"
echo ""
EOF'
chroot "$UBUNTU_ROOTFS" chown -R 1000:1000 /home/anon

# Copy the test script into the container
cp "$(dirname "$0")/../test_forkbomb.sh" "$UBUNTU_ROOTFS/home/anon/" 2>/dev/null || true
chroot "$UBUNTU_ROOTFS" chown 1000:1000 /home/anon/test_forkbomb.sh 2>/dev/null || true
chroot "$UBUNTU_ROOTFS" chmod +x /home/anon/test_forkbomb.sh 2>/dev/null || true

# Apply cgroup limits to current process before launching bwrap
if [ -n "$CGROUP_PATH" ]; then
  echo $$ > "$CGROUP_PATH/cgroup.procs" 2>/dev/null || true
fi

# Launch fully isolated shell as anon user
echo "[anonmal] Launching isolated shell environment..."
exec bwrap \
  --unshare-all \
  --share-net \
  --hostname "$HOSTNAME" \
  --ro-bind "$UBUNTU_ROOTFS" / \
  "${BWRAP_TMPFS_ARGS[@]}" \
  --dev-bind /dev/null /dev/null \
  --dev-bind /dev/zero /dev/zero \
  --dev-bind /dev/random /dev/random \
  --dev-bind /dev/urandom /dev/urandom \
  --tmpfs /dev/shm \
  --proc /proc \
  --tmpfs /sys \
  --die-with-parent \
  --new-session \
  --setenv HISTFILE /dev/null \
  --setenv TMPDIR /tmp \
  --setenv HOME /home/anon \
  --setenv USER anon \
  --setenv LOGNAME anon \
  --setenv SHELL /bin/bash \
  --setenv PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
  $ENV_VARS \
  --chdir /home/anon \
  --uid 1000 --gid 1000 \
  -- \
  bash -l