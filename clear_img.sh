#!/bin/bash

# Directory to clear
DIR="img"

# Check if the directory exists
if [ -d "$DIR" ]; then
    echo "Clearing contents of $DIR..."
    rm -rf "$DIR"/* "$DIR"/.[!.]* "$DIR"/..?*
    echo "Contents of $DIR have been deleted."
else
    echo "Directory $DIR does not exist."
fi
