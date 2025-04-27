#!/bin/bash

cd "$(dirname "$0")"

# Check if Docker container is running
if ! docker ps | grep -q osonai_container; then
  docker start osonai_container || docker run -d --name osonai_container -p 3000:3000 osonai
fi

# Open the web app
open http://localhost:3000
