#!/bin/bash

docker-compose down

git pull

docker-compose build
docker-compose up -d

sleep 10
docker logs messanger_api-api-1