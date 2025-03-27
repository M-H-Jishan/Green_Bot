#!/bin/bash

# Create SSL directory if it doesn't exist
mkdir -p ../ssl

# Generate private key and certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout ../ssl/privkey.pem \
  -out ../ssl/fullchain.pem \
  -subj "/CN=localhost"
