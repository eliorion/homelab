import os
import pulumi 
import pulumi_proxmoxve as proxmoxve
from . import common

class Proxmox:
    def __init__(self, node_name, api_token_id, api_token, endpoint, insecure=False):
        self._mac_addr_offset = 0
        self._vm_id_offset = 500
        self._node_name = node_name
        api_access = f"{api_token_id}={api_token}"
        self._proxmox_provider = self.__init_provider(node_name, endpoint, api_access, insecure)
        
    def createVm(self,
                deployement_name,                       # Name of the ressource Pulumi
                boot_file_id="local:iso/talos-os-metal-amd64.iso", 
                clone_vm_id=None,
                clone_datastore_id="homelab_storage",
                vm_name=None,
                machine="i440fx",
                ram_memory=1024,
                net_bridge="vmbr0",
                disksSize=[8]):
        pvm = proxmoxve.vm
        agentArgs = pvm.VirtualMachineAgentArgs(
             enabled=False,
             timeout="1m",
             trim=False,
             type="virtio",
             wait_for_ip={
                "ipv4": True,
                "ipv6": False,
             }
        )
        cdromArgs = pvm.VirtualMachineCdromArgs(
             file_id=boot_file_id
        )
        cloneArgs = pvm.VirtualMachineCloneArgs(
            vm_id=clone_vm_id,
            datastore_id=clone_datastore_id,
            full=True,
            node_name=self._node_name,
            retries=0
        )
        cpuArgs = pvm.VirtualMachineCpuArgs(
            cores=4,
            type="x86-64-v2-AES",
        )
        disksArgs = pvm.VirtualMachineDiskArgs(
             interface="scsi0",
             datastore_id=clone_datastore_id,
             size=disksSize[0]
        )
        cloudInitArgs = pvm.VirtualMachineInitializationArgs(
            datastore_id=clone_datastore_id,
            file_format=None,
            interface=None,
            ip_configs=[
                {
                    "ipv4": {
                        "address": None,
                        "gateway": None,
                    },
                    "ipv6": {
                        "address": None,
                        "gateway": None,
                    },
                },
            ],
            meta_data_file_id=None,
            network_data_file_id=None,
            type=None,
            user_account={
                "keys": [None],
                "password": None,
                "username": None,
            },
            user_data_file_id=None,
            vendor_data_file_id=None,
        )
        memoryArgs = pvm.VirtualMachineMemoryArgs(
            dedicated=ram_memory,
            floating=ram_memory,
        )
        networkArgs = pvm.VirtualMachineNetworkDeviceArgs(
            bridge=net_bridge,
            enabled=True,
            mac_address=self._gen_mac_addr(),
            queues=4,
        )
        serialArgs = pvm.VirtualMachineSerialDeviceArgs(
             device="socket"
        )
        usbArgs0 = pvm.VirtualMachineUsbArgs(
            host=None,
            mapping=None,
            usb3=True
        )
 
        return proxmoxve.vm.VirtualMachine(
            deployement_name,                  
            acpi=True,
            agent=None,
            cdrom=cdromArgs,
            cpu=cpuArgs,
            delete_unreferenced_disks_on_destroy=True,
            description="DevOps homelab node",
            disks=disksArgs,
            initialization=None,#cloudInitArgs,
            machine=None,#machine,
            memory=memoryArgs,
            migrate=False,
            name=vm_name,
            network_devices=[networkArgs],
            node_name=self._node_name,
            on_boot=True,
            purge_on_destroy=True,         
            reboot=False,
            reboot_after_update=False,
            serial_devices=[serialArgs],
            started=True,
            usbs=None,#[usbArgs0],
            vm_id=self._gen_vm_id(),
            
            opts=self._proxmox_provider
        )
    def upload_boot_fiile(self):
        pass

    def __init_provider(self,node_name, endpoint, api_access, insecure):
        provider = proxmoxve.Provider(
            node_name, 
            endpoint=endpoint, 
            api_token=api_access,
            insecure=insecure,
        )
        return pulumi.ResourceOptions(provider=provider)
         
    def _gen_mac_addr(self, prefix="BC:24:11"):
        offset = self._mac_addr_offset
        self._mac_addr_offset = self._mac_addr_offset
        return common.get_mac_address(prefix, offset)
         
    def _gen_vm_id(self):
        offset = self._vm_id_offset
        self._vm_id_offset = self._vm_id_offset + 1
        return offset

def test():
    """
    Test

    :param a: Le premier nombre.
    :param b: Le second nombre.
    :return: La somme de a et b.
    """
    print("ici")

# Add the membership to the pool homelab
"""
test_pool = proxmoxve.permission.Pool(
    pool_id, 
    pool_id=pool_id,
    opts=proxmox_access
    )


for vm in vms:
    vm_membership = proxmoxve.pool.Membership(
        f"{pool_id}_{vm[1]}",
        pool_id=pool_id,
        vm_id=vm[0].id,
        opts=proxmox_access
        )
"""