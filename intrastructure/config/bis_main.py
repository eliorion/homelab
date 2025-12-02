import pulumi
import pulumi_proxmoxve as proxmoxve

# Define a Proxmox VM template that will be used for the Kubernetes nodes
k8s_node_template = proxmoxve.vm.Qemu(
    "k8s-node-template",
    name="k8s-node-template",
    target_node="proxmox_node_name",
    disks=[{
        "size": "10G",
        "type": "ssd"
    }],
    cores=2,
    memory=4096,
    network_interfaces=[{
        "name": "eth0",
        "bridge": "vmbr0"
    }],
    os_type="cloud-init",
    os_template="local:vztmpl/ubuntu-20.04-template.qcow2"
)

# Define a function to create a new Kubernetes node
def create_k8s_node(name, node_number):
    return proxmoxve.vm.Qemu(
        name,
        name=f"k8s-node-{node_number}",
        clone=k8s_node_template.name,
        target_node="proxmox_node_name",
        disks=[{
            "size": "10G",
            "type": "ssd"
        }],
        cores=2,
        memory=4096,
        network_interfaces=[{
            "name": "eth0",
            "bridge": "vmbr0"
        }],
        os_type="cloud-init",
        os_network_config={
            "ip": f"192.168.1.{100+node_number}"
        }
    )

# Create 3 Kubernetes nodes
k8s_nodes = [create_k8s_node(f"k8s-node-{i+1}", i+1) for i in range(3)]

pulumi.export("k8s_nodes", [node.name for node in k8s_nodes])
