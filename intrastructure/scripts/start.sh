# /bin/bash

# Choose your container app
CONTAINER_TOOL="podman"
#CONTAINER_TOOL="docker"

setup_proxmox()
{
    export PROXMOX_VE_ENDPOINT=XXXXXXXXXXXX
    export PROXMOX_VE_PASSWORD=><Er@;:=
    export PROXMOX_VE_USERNAME=ZZZZZZZZZZZZ
    export PROXMOX_VE_INSECURE=AAAAAAAAAAAA
}

start_pulumi()
{
    $CONTAINER_TOOL run -it \
        -e PULUMI_ACCESS_TOKEN=pul-731fc64f1676e1cc5fdea001d893060bcbe10d93 \
        -w /app \
        -v $(pwd)/config:/app \
        --entrypoint bash \
        pulumi/pulumi:3.204.0-nonroot \
        #-c "ls"
        #-c "pulumi new kubernetes-python"
        #-c "pip install -r requirements.txt"
        # && pulumi preview --stack dev --non-interactive"
}


start_pulumi