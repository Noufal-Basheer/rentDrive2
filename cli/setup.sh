#!/bin/bash

# Check if script is run as root
if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root" 1>&2
    exit 1
fi

# Set umask to allow maximum permissions
umask 000

# Create /opt/.rentdrive directory if it doesn't exist
if [ ! -d "/opt/.rentdrive" ]; then
    echo "Creating /opt/.rentdrive directory..."
    mkdir -p /opt/.rentdrive
fi

# Set full permissions for /opt/.rentdrive directory
chmod 777 /opt/.rentdrive

# Set default ACL for /opt/.rentdrive directory
setfacl -R -m u::rwx,g::rwx,o::rwx /opt/.rentdrive

# Check if symbolic link exists and remove if so
if [ -L /usr/local/bin/rentdrive-cli ]; then
    echo "Removing existing symbolic link..."
    rm /usr/local/bin/rentdrive-cli
fi

# Change permissions for current directory
chmod u+wx,o+wx .

# Create new symbolic link
echo "Creating new symbolic link..."
ln -s "$(pwd)/rentdrive" /usr/local/bin/rentdrive-cli

echo "Setup complete."
