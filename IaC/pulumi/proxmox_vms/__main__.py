import os
import homelab_ressources.proxmox.vm_machine as proxmox
from homelab_ressources.proxmox.vm_machine import Proxmox

# Get environnement variables
proxmox_endpoint     = os.getenv("PROXMOX_VE_ENDPOINT")
proxmox_api_token    = os.getenv("PROXMOX_API_TOKEN")
proxmox_api_token_id = os.getenv("PROXMOX_API_TOKEN_ID")


# Initialise the proxmox provider
proxProvider = proxmox.Proxmox("proxmox", proxmox_api_token_id, proxmox_api_token, endpoint=proxmox_endpoint, insecure=True)

# Define the cluster vm
cluster = [
    {"name": "Controlplane", "ram": 4096, "disksSize": [16]},
    {"name": "Worker-1", "ram": 2048, "disksSize": [8]},
    {"name": "Worker-2", "ram": 2048, "disksSize": [8]},
#    {"name": "Load-balancer", "ram": 4096, "disksSize": [16]},
]

# Create the vm
for vm in cluster:
    proxProvider.createVm(vm["name"], vm_name=vm["name"], ram_memory=vm["ram"], disksSize=vm["disksSize"])