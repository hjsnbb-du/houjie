#!/bin/bash

# Load environment variables
set -a
source .env.prod
set +a

# Start the application
npm run start
