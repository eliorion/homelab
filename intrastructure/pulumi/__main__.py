import os
import pulumi
import pulumi_proxmoxve as proxmoxve

# Get environnement variables
proxmox_ip     = os.getenv("PROXMOX_IP")
proxmox_api_token    = os.getenv("PROXMOX_API_TOKEN")
proxmox_api_token_id = os.getenv("PROXMOX_API_TOKEN_ID")
proxmox_endpoint = f"https://{proxmox_ip}:8006/"
proxmox_api = f"{proxmox_api_token_id}={proxmox_api_token}"


# Settings for the Proxmox provider
proxmox_provider = proxmoxve.Provider("proxmox", 
    endpoint=proxmox_endpoint,  # Proxmox endpoint
    api_token=proxmox_api,  # API token secret
    insecure=True,

    #username=f"pulumi@pam"
)
"""
proxmox_provider = proxmoxve.Provider("proxmox",
    endpoint=proxmox_endpoint,
    password=f"",
    username=f"pulumi@pam",
    insecure=True,
)
"""
# Example: Get Proxmox version information
proxmox_version = proxmoxve.vm.get_virtual_machine(node_name="proxmox", vm_id=9000, opts=pulumi.InvokeOptions(provider=proxmox_provider))

# Export the Proxmox version information
pulumi.export("proxmox_version", proxmox_version.status)