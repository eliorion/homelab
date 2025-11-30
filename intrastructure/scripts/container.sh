# /bin/bash

PROJECT_DIR=(pwd)

build_local_container()
{
    podman build -t local/pulumi-python:1.0.0 -f $PROJECT_DIR/pulumi/Containerfile $PROJECT_DIR/pulumi/config
}

