#!/bin/bash

docker compose down
docker rmi playgrounds
docker compose up -d
docker compose logs -f