docker rmi `docker images -qa`  # no rollback??
docker pull $AP:$DOCKER_TAG
docker rename $PROJECT "$PROJECT.last" || echo "$PROJECT not found"
docker stop $PROJECT.last || echo "$PROJECT.last not found"
docker run --name $PROJECT \
    --restart=always \
    --env-file pointillism.env \
    -d -p $SERVICE_PORT:$SERVICE_PORT $ACCOUNT/$PROJECT:$DOCKER_TAG
docker rm $PROJECT.last
docker images prune
