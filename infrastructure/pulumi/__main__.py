import os
import pulumi
import pulumi_proxmoxve as proxmoxve
import proxmox_server

import random

def get_mac_address(nb, prefix="BC:24:11"):
    # On décompose le préfixe en octets déjà définis
    parts = prefix.split(":")
    prefix_len = len(parts)

    if prefix_len >= 6:
        raise ValueError("Prefix must contain fewer than 6 octets.")

    # Nombre d'octets à compléter
    remaining = 6 - prefix_len

    # Base numérique pour commencer l'incrément
    start = 0
    max_value = 256 ** remaining

    if nb > max_value:
        raise ValueError("Requested number exceeds the available MAC space with this prefix.")

    result = []
    for i in range(nb):
        value = i + start
        block = []
        for _ in range(remaining):
            block.insert(0, f"{value & 0xFF:02X}")
            value >>= 8
        mac = parts + block
        result.append(":".join(mac))

    return result

mac_address = get_mac_address(3)


# Get environnement variables
proxmox_ip     = os.getenv("PROXMOX_IP")
proxmox_api_token    = os.getenv("PROXMOX_API_TOKEN")
proxmox_api_token_id = os.getenv("PROXMOX_API_TOKEN_ID")
proxmox_endpoint = f"https://{proxmox_ip}:8006/"
proxmox_api = f"{proxmox_api_token_id}={proxmox_api_token}"


# Internal const
proxmox_node_name="proxmox"

# Settings for the Proxmox provider
proxmox_provider = proxmoxve.Provider(
    proxmox_node_name, 
    endpoint=proxmox_endpoint, # Proxmox endpoint
    api_token=proxmox_api,     # API token secret
    insecure=True,             # Unset the security http request
)

test_proxmox_access=pulumi.InvokeOptions(provider=proxmox_provider)
proxmox_access=pulumi.ResourceOptions(
    provider=proxmox_provider
    )

#pool_id=proxmoxve.permission.Pool("homelab", pool_id="homelab", opts=pulumi.InvokeOptions(provider=proxmox_provider))

pool_id="homelab"

# Define the control plane node and the worker nodes
nodes = [
    {"name": "control-plane", "vm_id": 101, "pool_id": pool_id, "MAC_address": mac_address[0]},
#    {"name": "worker-1", "vm_id": 102, "pool_id": pool_id, "MAC_address": mac_address[1]},
#    {"name": "worker-2", "vm_id": 103, "pool_id": pool_id, "MAC_address": mac_address[2]},
]

# Create virtual machines based on the existing template with ID 9000
vms = []
for node in nodes:
    vm = proxmoxve.vm.VirtualMachine(
        node["name"],                       # Name of the ressource Pulumi
        description="DevOps homelab node",
        name=node["name"],
        node_name=proxmox_node_name,        # The node name in Proxmox
        agent={
            "enabled": True,
            "timeout": "1m",
#            "trim": False,
#            "type": "virtio",
            "wait_for_ip": {
                "ipv4": True,
#                "ipv6": False,
            },
        },
#        cdrom={
#            "file_id": "local:iso/noble-server-cloudimg-amd64.img",
#            "interface": "ide0",
#        },
        clone={
            "vm_id": 9000,
            "full": True,
            "node_name": proxmox_node_name,
            "datastore_id": "homelab_storage",
            "retries": 1,
        },
        cpu={
            #"affinity": "",
            #"architecture": "x86_64",
            "cores": 4,
            "flags": [],
            "hotplugged": 0,
            "limit": 0,
            "numa": False,
            "sockets": 1,
            "type": "x86-64-v2-AES",
            "units": 1024,
        },
        initialization={
            "datastore_id": "homelab_storage",
            #"file_format": "string",
            "interface": "ide2",
            "ip_configs": [
                {
                    "ipv4": {
                        "address": "192.168.1.210/24",
                        "gateway": "192.168.1.1",
                    },
                    "ipv6": {
                        "address": "dhcp",
                        "gateway": "",
                    },
                },
            ],
            #"meta_data_file_id": "string",
            #"network_data_file_id": "string",
            #"type": "string",
            "user_account": {
                "keys": ["ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGd/hnLK+94QSPjBnTP90aWb16GTTr0GXvtwGCSMEENV vscode@d08f9066d2c3"],
                "password": "root",
                "username": "devops",
            },
            #"user_data_file_id": "/var/lib/vz/template/snippets",
            #"vendor_data_file_id": "",
        },
        memory={
            "dedicated": 4096,
            "floating": 4096,
#            "shared": 1000,
        },
        network_devices=[{
            "bridge": "vmbr0",
            "mac_address": node["MAC_address"],
            "queues": 4,
        }],
        on_boot=True,
        reboot=True,
        reboot_after_update=True,
        vm_id=node["vm_id"],
        #pool_id=pool_id,
        started=True,                       # Start the VM immediately after creation
        opts=proxmox_access                 # Access to the Proxmox server
    )
    vms.append([vm, node["name"]])

# Add the membership to the pool homelab
"""
test_pool = proxmoxve.permission.Pool(
    pool_id, 
    pool_id=pool_id,
    opts=proxmox_access
    )
"""

for vm in vms:
    vm_membership = proxmoxve.pool.Membership(
        f"{pool_id}_{vm[1]}",
        pool_id=pool_id,
        vm_id=vm[0].id,
        opts=proxmox_access
        )
