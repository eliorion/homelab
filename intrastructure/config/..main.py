import os
import pulumi
import pulumi_proxmox as proxmox

# Get environnement variables
proxmox_api_token = os.getenv("PROXMOX_API_TOKEN")

# Proxmox provider
provider = proxmox.

# Configuration
config = pulumi.Config()
ssh_public_key = config.require("sshKey") # Set via: pulumi config set sshKey "..."

# Common VM Specs
vm_specs = {
    "target_node": "pve", 
    "clone": "ubuntu-cloud-template", # ID 9000 from previous guide
    "cores": 2,
    "memory": 4096,
    "disk_size": "20G",
    "gateway": "192.168.1.1",
    "storage": "local-lvm"
}

# Define Nodes: Name -> IP ending
nodes = {
    "M00-control": "50",    # 192.168.1.50
    "M01-worker": "51",  # 192.168.1.51
    "M02-worker": "52"   # 192.168.1.52
}

for name, ip_suffix in nodes.items():
    proxmox.VmQemu(name,
        name=name,
        target_node=vm_specs["target_node"],
        clone=vm_specs["clone"],
        agent=1,
        os_type="cloud-init",
        cores=vm_specs["cores"],
        memory=vm_specs["memory"],
        scsihw="virtio-scsi-pci",
        boot="order=scsi0",
        disks=[{
            "storage": vm_specs["storage"],
            "size": vm_specs["disk_size"],
            "type": "scsi",
        }],
        network_interfaces=[{
            "model": "virtio",
            "bridge": "vmbr0",
        }],
        # Cloud Init setup
        ciuser="devops",
        sshkeys=ssh_public_key,
        # ipconfig0 format depends on provider version, usually:
        ipconfig0=f"ip=192.168.1.{ip_suffix}/24,gw={vm_specs['gateway']}"
    )

pulumi.export("master_ip", "192.168.1.50")

# Create the Proxmox provider instance with required configurations
proxmox_provider = proxmox.Provider('proxmoxve', 
    endpoint=pulumi.Config().require('PROXMOX_VE_ENDPOINT'),
    insecure=pulumi.Config().require('PROXMOX_VE_INSECURE') == 'true',
    username=pulumi.Config().require('PROXMOX_VE_USERNAME'),
    password=pulumi.Config().require('PROXMOX_VE_PASSWORD')
)

# Define any additional arguments if necessary (none in this case)
args = {}

# Create a virtual machine resource
vm = proxmox.vm.VirtualMachine('vm',
    args,
    opts=pulumi.ResourceOptions(provider=proxmox_provider)
)
