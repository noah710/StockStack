#!/bin/bash
IMAGE_NAME=webprog-flaskapp

if [[ ${1} == "fresh" ]]; then
    docker build --no-cache -f deploy/Dockerfile -t ${IMAGE_NAME} .
else
    docker build -f deploy/Dockerfile -t ${IMAGE_NAME} .
fi

docker run -it -p 8080:8080 -v `pwd`/src:/flask-src ${IMAGE_NAME} 
