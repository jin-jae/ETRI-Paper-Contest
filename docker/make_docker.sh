# docker build
docker build \
    -t lifelog:latest \
    .

# docker run
docker run \
    --gpus all \
    -it \
    -p 4242:4242 \
    --ipc=host \
    --name lifelog \
    -v ..:/workspace \
    lifelog:latest \
    /bin/bash
