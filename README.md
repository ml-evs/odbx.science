# odbx.science

[![OPTiMaDe](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Materials-Consortia/optimade-python-tools/master/.ci/optimade-version.json&logo=json)](https://github.com/Materials-Consortia/OPTiMaDe/) 
[![OPTiMaDe-compliant](https://img.shields.io/github/workflow/status/ml-evs/odbx.science/Scheduled%20validator?logo=github)](https://github.com/ml-evs/odbx.science/actions?query=branch%3Amaster+)

This repo contains some notes about the server running at odbx.science. 

This implementation of an OPTiMaDe server builds upon the reference server in
the following way:

- Additional routes from `odbx.science/<endpoint>` that mimic `odbx.science/optimade/<endpoint>` but
  provides rich HTML displays of the data.

## Hardware 

As of 02/12/19, the server runs as an HPCS OpenStack VM (quadcore Haswell, 8 GB RAM), with three virutal disks attached:

- `/dev/vda`, 80 GB, mounted at `/` contains OS and apps
- `/dev/vdb`, 1 TB, mounted at `/data/sql`, contains SQL database for OQMD
- `/dev/vdc`, 500 GB, mounted at `/data/mongo`, contains our MongoDB.

## Services & security

- `sshd` with password authentication and root login disabled, on port 22.
- `mongod` runs on the default port (which is closed) with authentication disabled, runs as an unpriveleged user and hosts the `crystals` database and various collections.
- `uvicorn`, the web server, runs as an unpriveleged user on port 5000. `iptables` forwards all port 80 traffic to port 5000, but must be reenabled at startup.
- `fail2ban` adds an extra layer of protection to `ssh` by banning password scrapers after a few attempts.
- `mysql` can be enabled to update the OQMD copy, but is not on by default.

## Software

- Currently the VM hosts a nearly default [MaterialsConsortia/optimade-python-tools](https://github.com/Materials-Consortia/optimade-python-tools) server that points to a MongoDB created by the converter in [ml-evs/matador_optimade](https://github.com/ml-evs/matador_optimade).
- JSON responses are served by the `uvicorn` web server, which is using FastAPI, Starlette and pydantic under the hood.

## Domains & SSL

- The domain `odbx.science` was purchased until 2023 from Namecheap, which currently redirects to the public IP of the VM.
- All `*@odbx.science` email addresses currently redirect to my personal account.
- The domain came with a 1 year SSL certificate (~£4 year after), but free alternatives exists (consider e.g. `cert-bot`).


## To-do

- [ ] Investigate a "proper" web server/reverse proxy, e.g. `nginx` or `traefik`
- [ ] Use Jinja2 templating engine to provide rich single-entry and multi-entry endpoints
