# Pulumi-infra
First Pulumi infrastructures for Proxmox homelab.
Pulumi is an Infrastructure as Code tool.


## Flux
You need to generate ssh keys, and than use `flux bootstrap` like this :
```bash
flux bootstrap git \        
  --url=ssh://git@github.com/USERNAME/REPOSITORY.git \
  --password=YOUR_SSH_PASSPHASE \
  --ssh-key-algorithm=SPECOFIC_ALGORITHM \
  --private-key-file=YOUR_PRIVATE_KEY_FILE \
  --branch=YOUR_BRANCH \
  --path=YOUR_PATH_SYNC
```