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
cluster1 = [
    {"name": "Controlplane", "ram": 4096, "disksSize": [16], "iso": "talos-os-metal-amd64.iso"},
    {"name": "Worker-1", "ram": 2048, "disksSize": [8], "iso": "talos-os-metal-amd64.iso"},
    {"name": "Worker-2", "ram": 2048, "disksSize": [8], "iso": "talos-os-metal-amd64.iso"},
]

# Define the cluster vm
cluster2 = [
        {"name": "Controlplane", "ram": 4096, "disksSize": [16], "iso": "talos-os-metal-amd64.iso"},
]

# Create the vm
for vm in cluster1:
    proxProvider.createVm(vm["name"], vm_name=vm["name"], ram_memory=vm["ram"], disksSize=vm["disksSize"])
