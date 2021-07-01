#! /usr/bin/env bash

# Let the DB start
python wait-for-postgres.py;
# Run migrations
alembic upgrade head
