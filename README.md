# Homelab
This project is a personal laboratory for my DevSecOps, Cloud, and GitOps learning journey.

## Tools use (Non-exhaustive list)
### Development
| Type | Tools | Curently use | Commentary |
|------|-------|:------------:|------------|
| Container development | Devcontainer | 🟢 | Use for installing all the tools requested for the project |
| Devcontainer manager | Devpod | 🟢 | Manage the Devcontainer and add my own dotfiles to the container |
| Environment manager | Direnv | 🟢 | Simplify the load and unload of my .envrc files |

### Infrastructure
| Type | Tools | Curently use | Commentary |
|------|-------|:------------:|------------|
| VM provider | Proxmox | 🟢| Single server for now |
| VM | Talos linux | 🟢 | Three nodes deplyed |
| IaC | Pulumi | 🟢 | Used to provision my Proxmox VMs |

###  Base CI/CD 
| Type | Tools | Curently use | Commentary |
|------|-------|:------------:|------------|
| Container manager | Kubernetes | 🟠 | Currently learning and experimenting |
| Data storage | TrueNAS | 🟠 | Use as external persistant data for the cluster. Run on Proxmox |
| External internet access | Cloudflaire tunneling | 🟠 | Currently learning and experimenting |
| CI/CD | GitHub Action | 🔴 | Will be used once my first application is ready|
| GitOps | Flux | 🔴 | Planned once I reach a stronger understanding of Kubernetes |

### Extended DevSecOps
I will integrate the `Sec`  part of `DevSecOps` after my first full pipeline is operational and my website is publicly accessible. At this stage, I am still exploring which security tools and practices I will include in the pipeline.
| Type | Tools | Curently use | Commentary |
|------|-------|:------------:|------------|
| Container scan |  | 🔴 | Scan the container before the deployment |

## Kubernetes
### Addons
| Type | Name | Learning stat | Commentary |
|------|------|---------------|------------|
| CSI | nfs-driver | 🟢 | In place to use the TrueNAS NFS share files |
| CNI | Traefix | 🟠 | Learning |
| K8 API | API gateway | 🟠 | Learning |
| Persistance data manager | Longhorn | 🔴 | Will be used when I will have real nodes (note VM) cluster |


## Applications stack
Regroup the applications who run or will run on my homelab.
| Type | App | Curently use | Commentary |
|------|-------|:------------:|------------|
| IT asset management | GLPI | 🟠 | Curently in developement |
| ERP | ERP Next | 🔴 | Just for testing functionnality |
| CloudApp | NextCloud | 🔴 | Will be used for my personal and family usage |
| Custom | Scraping | 🔴 | Tool to scrape data on a site and use IA for recommendation purposes |
