#!/bin/bash

docker compose down
docker rm playgrounds
docker rmi playgrounds
# sudo rm app/db_files/*.db
# docker system prune -a -f
docker compose up -d
docker compose logs -f