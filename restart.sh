#!/bin/bash

docker compose down
docker rmi playgrounds
# rm -f src/blog.db
# rm -f src/user.db
docker compose up -d
docker compose logs -f
