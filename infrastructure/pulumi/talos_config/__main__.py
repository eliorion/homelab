import os
import pulumi
import pulumi_command as command
import pulumiverse_talos as talos
import pulumi_kubernetes as k8s

# Stack reference to ProxmoxVms
config = pulumi.Config()
org = config.require("org")
stack = pulumi.get_stack()

proxmox_stack = pulumi.StackReference(f"{org}/ProxmoxVms/{stack}")

# Get environement var
control_plane_ip = os.getenv("CONTROL_PLANE_IP")
worker_ip        = os.getenv("WORKER_IP")
cluster_name     = os.getenv("CLUSTER_NAME")
disk_name        = os.getenv("DISK_NAME")

nodes = [
    {"ip": control_plane_ip, "config": ""},
    {"ip": "192.168.1.43", "config": ""}
]


gen_conf = command.local.Command(
    "talos-conf-gen",
    create=f"talosctl gen config {cluster_name} https://{nodes[0]['ip']}:6443 --install-disk /dev/{disk_name} --output ./configs --force",
    update=""
)

apply_conf_controlplane = command.local.Command(
    "talos-apply-conf-controlplane",
    create=f"talosctl apply-config --insecure --nodes {control_plane_ip} --file ./configs/controlplane.yaml",
    opts=pulumi.ResourceOptions(parent=gen_conf),
    update=""
)

apply_conf_worker = command.local.Command(
    "talos-apply-conf-worker-",
    create=f"talosctl apply-config --insecure --nodes {worker_ip} --file ./configs/worker.yaml",
    opts=pulumi.ResourceOptions(parent=apply_conf_controlplane),
    update=""
)

set_endpoint = command.local.Command(
    "talos-set-endpoint",
    create=f"talosctl --talosconfig=./configs/talosconfig config endpoints {control_plane_ip}",
    opts=pulumi.ResourceOptions(parent=apply_conf_worker),
    update=""
)

wait_booting = command.local.Command(
    "talos-wait-booting",
    create=f"sleep 20",
    opts=pulumi.ResourceOptions(parent=set_endpoint),
    update=""
)

bootstrap = command.local.Command(
    "talos-bootstrap",
    create=f"talosctl bootstrap --nodes {control_plane_ip} --talosconfig=./configs/talosconfig",
    opts=pulumi.ResourceOptions(parent=wait_booting),
    update=""
)

get_kubernetes_access = command.local.Command(
    "talos-get-kubernetes-access",
    create=f"talosctl kubeconfig configs/kubeconfig --nodes {control_plane_ip} --talosconfig=./configs/talosconfig",
    opts=pulumi.ResourceOptions(parent=bootstrap),
    update=""
)

check_health = command.local.Command(
    "talos-check-health",
    create=f"talosctl --nodes {control_plane_ip} --talosconfig=./configs/talosconfig health",
    opts=pulumi.ResourceOptions(parent=get_kubernetes_access),
)

"""
with open("./configs/controlplane.yaml") as f:
    cp_config = f.read()

with open("./configs/worker.yaml") as f:
    w_config = f.read()


cp_apply = talos.machine.ConfigurationApply(
    "apply-cp",
    node=node[0]['ip'],
    config=cp_config,
)

worker_apply = talos.machine.ConfigurationApply(
    "apply-worker",
    node=node[1]['ip'],
    config=w_config,
)


bootstrap = talos.machine.Bootstrap(
    "bootstrap",
    node=node[0]['ip'],
    opts=pulumi.ResourceOptions(depends_on=[cp_apply]),
)


kubeconfig = talos.cluster.Kubeconfig(
    "kubeconfig",
    node=node[0]['ip'],
    opts=pulumi.ResourceOptions(depends_on=[bootstrap]),
)




cp_ip = "192.168.1.42"
worker_ip = "192.168.1.43"
endpoint = f"https://{cp_ip}:6443"


controlplane = talos.Configuration(
    "controlplane",
    cluster_name=cluster_name,
    machine_type="controlplane",
    endpoint=endpoint,
    nodes=[cp_ip],
)

worker = talos.Configuration(
    "worker",
    cluster_name=cluster_name,
    machine_type="worker",
    endpoint=endpoint,
    nodes=[worker_ip],
)

apply_cp = talos.MachineConfigurationApply(
    "applyCP",
    node=cp_ip,
    config=controlplane.machine_configuration,
)

apply_worker = talos.MachineConfigurationApply(
    "applyWorker",
    node=worker_ip,
    config=worker.machine_configuration,
)

bootstrap = talos.ClusterBootstrap(
    "bootstrap",
    node=cp_ip,
    opts=pulumi.ResourceOptions(depends_on=[apply_cp]),
)

kubeconfig = talos.Kubeconfig(
    "kubeconfig",
    node=cp_ip,
    opts=pulumi.ResourceOptions(depends_on=[bootstrap]),
)

k8s_provider = k8s.Provider(
    "k8s",
    kubeconfig=kubeconfig.kubeconfig,
)

k8s.yaml.ConfigFile(
    "calico",
    file="https://raw.githubusercontent.com/projectcalico/calico/v3.27.0/manifests/calico.yaml",
    opts=pulumi.ResourceOptions(provider=k8s_provider),
)



secrets = talos.machine.Secrets("secrets")

talos.Configuration

configuration = talos.machine.get_configuration_output(cluster_name="exampleCluster",
    machine_type="controlplane",
    cluster_endpoint=f"https://{node[0]['ip']}:6443",
    machine_secrets=secrets.machine_secrets)

configuration_apply = talos.machine.ConfigurationApply("configurationApply",
    client_configuration=secrets.client_configuration,
    machine_configuration_input=configuration.machine_secrets,
    node=node[0]["ip"],
    config_patches=[json.dumps({
        "machine": {
            "install": {
                "disk": "/dev/sdd",
            },
        },
    })])
bootstrap = talos.machine.Bootstrap("bootstrap",
    node=node[0]["ip"],
    client_configuration=secrets.client_configuration,
    opts=pulumi.ResourceOptions(depends_on=[configuration_apply]))
"""