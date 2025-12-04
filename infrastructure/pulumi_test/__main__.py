import os
import yaml
import pulumi
import pulumi_proxmoxve as proxmox

# Get environnement variables
proxmox_ip     = os.getenv("PROXMOX_IP")
proxmox_api_token    = os.getenv("PROXMOX_API_TOKEN")
proxmox_api_token_id = os.getenv("PROXMOX_API_TOKEN_ID")
proxmox_endpoint = f"https://{proxmox_ip}:8006/"
proxmox_api = f"{proxmox_api_token_id}={proxmox_api_token}"


# Internal const
proxmox_node_name="proxmox"

# Settings for the Proxmox provider
proxmox_provider = proxmox.Provider(
    proxmox_node_name, 
    endpoint=proxmox_endpoint, # Proxmox endpoint
    api_token=proxmox_api,     # API token secret
    insecure=True,             # Unset the security http request
)

test_proxmox_access=pulumi.InvokeOptions(provider=proxmox_provider)
proxmox_access=pulumi.ResourceOptions(
    provider=proxmox_provider
    )

with open('vms.yaml', 'r') as file:
    yaml_content = file.read()

parsed_data = yaml.safe_load(yaml_content)

for vm in parsed_data['vms']:
    disks = []
    nets = []
    ip_configs = []
    ssh_keys = []

    for disk_entry in vm.get('disks', []):
        disk = disk_entry.popitem()[1]
        disks.append(
            proxmox.vm.VirtualMachineDiskArgs(
                interface=disk.get('interface', ''),
                datastore_id=disk.get('datastore_id', ''),
                size=disk.get('size', 0),
                file_format=disk.get('file_format', ''),
                cache=disk.get('cache', ''),
            )
        )

    for ip_config_entry in vm['cloud_init']['ip_configs']:
        ipv4 = ip_config_entry.get('ipv4')
        ipv6 = ip_config_entry.get('ipv6')

        if ipv4:
            ip_configs.append(
                proxmox.vm.VirtualMachineInitializationIpConfigArgs(
                    ipv4=proxmox.vm.VirtualMachineInitializationIpConfigIpv4Args(
                        address=ipv4.get('address', ''),
                        gateway=ipv4.get('gateway', '')
                    ),

                )
            )

        if ipv6:
            ip_configs.append(
                proxmox.vm.VirtualMachineInitializationIpConfigArgs(
                    ipv6=proxmox.vm.VirtualMachineInitializationIpConfigIpv6Args(
                        address=ipv6.get('address', ''),
                        gateway=ipv6.get('gateway', ''),
                    )
                )
            )

    for ssk_keys_entry in vm['cloud_init']['user_account']['keys']:
        ssh_keys.append(ssk_keys_entry)


    for net_entry in vm.get('network_devices', []):
        net = net_entry.popitem()[1]
        nets.append(
            proxmox.vm.VirtualMachineNetworkDeviceArgs(
                bridge=net.get('bridge', ''),
                model=net.get('model', ''),
            )
        )

    virtual_machine = proxmox.vm.VirtualMachine(
        vm_id=vm['vm_id'],
        resource_name=vm['resource_name'],
        node_name=vm['node_name'],
        agent=proxmox.vm.VirtualMachineAgentArgs(
            enabled=vm['agent']['enabled'],
            trim=vm['agent']['trim'],
            type=vm['agent']['type'],
        ),
        bios=vm['bios'],
        cpu=proxmox.vm.VirtualMachineCpuArgs(
            cores=vm['cpu']['cores'],
            sockets=vm['cpu']['sockets'],
        ),
        clone=proxmox.vm.VirtualMachineCloneArgs(
            node_name=vm['clone']['node_name'],
            vm_id=vm['clone']['vm_id'],
            full=vm['clone']['full'],
        ),
        disks=disks,
        memory=proxmox.vm.VirtualMachineMemoryArgs(
            dedicated=vm['memory']['dedicated'],
        ),
        name=vm['name'],
        network_devices=nets,
        initialization=proxmox.vm.VirtualMachineInitializationArgs(
            type=vm['cloud_init']['type'],
            datastore_id=vm['cloud_init']['datastore_id'],
            ip_configs=ip_configs,
            user_account=proxmox.vm.VirtualMachineInitializationUserAccountArgs(
                username=vm['cloud_init']['user_account']['username'],
                password=vm['cloud_init']['user_account']['password'],
                keys=ssh_keys,
            ),
        ),
        on_boot=vm['on_boot'],
        opts=proxmox_access
    )
    
    pulumi.export(vm['name'], virtual_machine.id)