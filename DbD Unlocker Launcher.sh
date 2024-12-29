#!/bin/bash

SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
PYTHON_COMMAND="~/.venv/bin/python3 \"$SCRIPT_DIR/main.py\""

if command -v x-terminal-emulator &> /dev/null; then
    x-terminal-emulator -e bash -c "$PYTHON_COMMAND; exec bash"
elif command -v gnome-terminal &> /dev/null; then
    gnome-terminal -- bash -c "$PYTHON_COMMAND; exec bash"
elif command -v konsole &> /dev/null; then
    konsole --hold -e bash -c "$PYTHON_COMMAND"
elif command -v xterm &> /dev/null; then
    xterm -hold -e bash -c "$PYTHON_COMMAND"
else
    echo "Error try to launch main.py manually with python"
    exit 1
fi
