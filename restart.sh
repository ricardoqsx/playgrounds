#!/bin/bash

docker compose down
docker rmi playgrounds
# docker system prune -a -f
# rm -f src/blog.db
# rm -f src/user.db
ruta="src"
sudo find "$ruta" -type d -name "__pycache__" -exec rm -rf {} +
docker compose up -d
docker compose logs -f
