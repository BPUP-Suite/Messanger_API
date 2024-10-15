#!/bin/bash

docker-compose build
docker-compose up -d

sleep 5
docker logs messanger_api-api-1