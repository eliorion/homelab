import os
import pulumi
import pulumi_proxmoxve as proxmoxve

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
    {"name": "control-plane", "vm_id": 101, "pool_id": pool_id},
#    {"name": "worker-1", "vm_id": 102, "pool_id": pool_id},
#    {"name": "worker-2", "vm_id": 103, "pool_id": pool_id},
]

# Create virtual machines based on the existing template with ID 9000
vms = []
for node in nodes:
    vm = proxmoxve.vm.VirtualMachine(
        node["name"],                       # Name of the ressource Pulumi
        description="DevOps homelab node",
        name=node["name"],
        node_name=proxmox_node_name,        # The node name in Proxmox
        acpi=True,
#        agent={
#            "enabled": False,
#            "timeout": "string",
#            "trim": False,
#            "type": "string",
#            "wait_for_ip": {
#                "ipv4": False,
#                "ipv6": False,
#            },
#        },
#        amd_sev={
#            "allow_smt": True,
#            "kernel_hashes": False,
#            "no_debug": False,
#            "no_key_sharing": False,
#            "type": "std",
#        },
        audio_device={
            "device": "intel-hda",
            "driver": "spice",
            "enabled": False,
        },
        bios="seabios",
        boot_orders=["ide0"],
        cdrom={
            "file_id": "local:iso/jammy-server-cloudimg-amd64.img",
            "interface": "ide0",
        },
#        clone={
#            "vm_id": 0,
#            "datastore_id": "string",
#            "full": False,
#            "node_name": "string",
#            "retries": 0,
#        },
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
        delete_unreferenced_disks_on_destroy=True,
        disks=[
            # Storage disk
            {
                "interface": "virtio0",
                #"discard": "string",
                "replicate": True,
                "datastore_id": "homelab_storage",
                "aio": "io_uring",
                #"file_format": "string",
                #"file_id": "string",
                #"cache": "",
                "iothread": False,
                #"import_from": "string",
                #"path_in_datastore": "string",
                "backup": True,
                "serial": "01234",
                "size": 32,
                "speed": {
                    "iops_read": 0,
                    "iops_read_burstable": 0,
                    "iops_write": 0,
                    "iops_write_burstable": 0,
                    "read": 0,
                    "read_burstable": 0,
                    "write": 0,
                    "write_burstable": 0,
                },
                "ssd": False,
            },
        ],
        initialization={
            "datastore_id": "homelab_storage",
            #"file_format": "string",
            "interface": "ide2",
            "ip_configs": [
                {
                    "ipv4": {
                        "address": "dhcp",
                        "gateway": "",
                    },
                    "ipv6": {
                        "address": "dhcp",
                        "gateway": "",
                    },
                }
            ],
            #"meta_data_file_id": "string",
            #"network_data_file_id": "string",
            #"type": "string",
            "user_account": {
                "keys": ["ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIICuZeBqQylhlF705N5vkh23im6mUe/Y1Mnx0wxzk8fH vscode@6813a5afa6ae"],
                "password": "",
                "username": "devops",
            },
            #"user_data_file_id": "/var/lib/vz/template/snippets",
            #"vendor_data_file_id": "",
        },
        machine="pc",
        memory={
            "dedicated": 4096,
            "floating": 4096,
#            "shared": 1000,
        },
        network_devices=[{
            "bridge": "vmbr0",
            "mac_address": "BC:24:11:94:6F:44",
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


# Export Proxmox version information and VM details
proxmox_version = proxmoxve.vm.get_virtual_machine(
    node_name=proxmox_node_name, 
    vm_id=9000, 
    template=True, 
    opts=test_proxmox_access
    )

pulumi.export("proxmox_version", proxmox_version.status)







