#!/bin/bash
# build.sh

echo "Building GAMBIH Backend..."

# Install dependencies
pip install -r requirements.txt

# check for migrations
python manage.py makemigrations

# Run migrations
python manage.py migrate


# Collect static files
python manage.py collectstatic --noinput

echo "Build completed!"