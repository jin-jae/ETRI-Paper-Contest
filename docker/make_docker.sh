display_usage() { 
	echo "usage: ./make_docker.sh \$PATH_TO_GIT_REPO"
}

# docker build
docker build \
    -t lifelog \
    -f docker/Dockerfile \
    .

if [  $# -le 0 ] 
then 
    display_usage
    exit 1
fi

# docker run
docker run \
    --gpus all \
    -it \
    -p 4242:4242 \
    --ipc=host \
    --name lifelog \
    -v $1:/workspace \
    lifelog \
    /bin/bash
