#!/bin/bash

docker compose down
docker rm playgrounds
docker rmi playgrounds
docker compose up -d
docker compose logs -f