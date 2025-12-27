#!/bin/bash

echo "🔧 Running post-installation script..."

# Get the username of the user who invoked sudo
if [ "$SUDO_USER" ]; then
    USER_HOME=$(getent passwd "$SUDO_USER" | cut -d: -f6)
else
    USER_HOME="$HOME"
fi

APP_DIR="$USER_HOME/.local/share/applications"

# Ensure directory exists
mkdir -p "$APP_DIR"

# Copy the .desktop file
if [ -f "/usr/share/applications/wallpy.desktop" ]; then
    cp /usr/share/applications/wallpy.desktop "$APP_DIR/wallpy.desktop"
fi

# Update desktop database (ignore errors)
update-desktop-database "$APP_DIR" 2>/dev/null || true

echo "✅ Desktop entry installed to $APP_DIR"
