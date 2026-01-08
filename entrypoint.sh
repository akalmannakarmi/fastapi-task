#!/bin/sh

# Run migrations
alembic upgrade head

# Start app
exec "$@"
