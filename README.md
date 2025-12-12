# Pulumi-infra
First Pulumi infrastructures for Proxmox homelab.
Pulumi is an Infrastructure as Code tool.
# Homelab
This project is a personal laboratory for my DevSecOps, Cloud, and GitOps learning journey.

## Tools use (Non-exhaustive list)
| Type | Tools | Curently use | Commentary |
|------|-------|--------------|------------|
| VM provider | Proxmox | 🟢| Single server for now |
| VM | Talos linux | 🟢 | Three nodes deplyed |
| IaC | Pulumi | 🟢 | Used to provision my Proxmox VMs |
| Container manager | Kubernetes | 🟢 | Currently learning and experimenting |
| External internet access | Cloudflaire tunneling | 🟠 | Currently learning and experimenting |
| CI/CD | GitHub Action | 🔴 | Will be used once my first application is ready|
| GitOps | Flux | 🔴 | Planned once I reach a stronger understanding of Kubernetes |


I will integrate the `Sec`  part of `DevSecOps` after my first full pipeline is operational and my website is publicly accessible. At this stage, I am still exploring which security tools and practices I will include in the pipeline.

## Kubernetes
### Addons
| Type | Name | Commentary |
|------|-------|-----------|
| CNI | Traefix | Learning |
| K8 API | API gateway | Learning |
