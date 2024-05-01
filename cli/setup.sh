#!/bin/bash


if [ -L /usr/local/bin/rentdrive-cli ]; then
    echo "Removing existing symbolic link..."
    rm /usr/local/bin/rentdrive-cli
fi

chmod u+wx,o+wx .

echo "Creating new symbolic link..."
ln -s "$(pwd)/rentdrive" /usr/local/bin/rentdrive-cli

echo "Setup complete."
