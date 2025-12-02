import os
import pulumi
import pulumi_proxmoxve as proxmoxve

# Get environnement variables
proxmox_ip     = os.getenv("PROXMOX_IP")
proxmox_api_token    = os.getenv("PROXMOX_API_TOKEN")
proxmox_api_token_id = os.getenv("PROXMOX_API_TOKEN_ID")
proxmox_endpoint = "https://" + proxmox_ip + ":8006/api2/json"

# Settings for the Proxmox provider
proxmox_provider = proxmoxve.Provider("proxmox", 
    endpoint=proxmox_endpoint,  # Proxmox endpoint
    token_id=proxmox_api_token_id,  # PI token ID
    token_secret=proxmox_api_token  # API token secret
)

# Example: Get Proxmox version information
proxmox_version = proxmoxve.get_version({}, opts=pulumi.InvokeOptions(provider=proxmox_provider))

# Export the Proxmox version information
pulumi.export("proxmox_version", proxmox_version.version)
