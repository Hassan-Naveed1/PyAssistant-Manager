#!/bin/bash

# Here I am updating and installing required packages
echo "Checking and installing dependencies..."
sudo apt update
sudo apt install -y net-tools

# Here I am setting the VNC password
mkdir -p ~/.vnc
x11vnc -storepasswd mysecret123 ~/.vnc/passwd

# Here I am checking if noVNC is already present or needs to be cloned
NOVNC_PATH="/home/$USER/novnc"
if [ ! -d "$NOVNC_PATH" ]; then
    echo "noVNC not found. Downloading..."
    git clone https://github.com/novnc/noVNC.git "$NOVNC_PATH"
    echo "noVNC cloned to $NOVNC_PATH"
else
    echo "noVNC already exists."
fi

# Here I am checking if a graphical session is available before starting VNC
export DISPLAY=:0
if [ -n "$(pgrep X)" ] || [ -f /home/$USER/.Xauthority ]; then
    echo "Desktop session detected. Starting VNC..."

    x11vnc -display :0 -auth guess -rfbauth ~/.vnc/passwd -forever -shared -rfbport 5901 &
    echo "x11vnc started on :0 (5901)"

    if command -v websockify >/dev/null 2>&1; then
        websockify --web="$NOVNC_PATH" 6080 localhost:5901 &
        echo "websockify running on port 6080"
    else
        echo "websockify is not installed. Run: sudo apt install websockify"
    fi
else
    echo "No graphical session found (DISPLAY=:0). Please log into the desktop."
fi
