#!/bin/bash

docker compose down
docker rmi playgrounds
rm -f src/contacts.db
docker compose up -d
docker compose logs -f
