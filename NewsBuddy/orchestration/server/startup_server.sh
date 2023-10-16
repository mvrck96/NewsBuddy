#!/bin/bash
set -e  # Stop script on error

# Execute the initial command (original entrypoint)
prefect server start "$@" &

# Wait for the server to start
sleep 5  # Adjust accordingly

# Execute additional commands
prefect config set PREFECT_API_URL=${PREFECT_API_URL}

python create_blocks.py
# Keep the script running
wait $!
