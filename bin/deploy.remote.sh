export ENV=PROD
export ACCOUNT=pointillism
export PROJECT=pointillism
export SERVICE_PORT=5001
export AP=$ACCOUNT/$PROJECT

docker rmi `docker images -qa`  # no rollback??
docker pull $AP:latest
docker rename $PROJECT "$PROJECT.last"
docker stop $PROJECT.last
docker run --name $PROJECT \
    --restart=always \
    --env-file pointillism.env \
    -d -p $SERVICE_PORT:$SERVICE_PORT $ACCOUNT/$PROJECT:latest
docker rm $PROJECT.last
docker images prune
