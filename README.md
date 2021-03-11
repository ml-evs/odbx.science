# odbx.science

[![OPTIMADE](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Materials-Consortia/optimade-python-tools/v0.13.3/optimade-version.json)](https://github.com/Materials-Consortia/OPTIMADE/)
[![Build Status](https://img.shields.io/github/workflow/status/ml-evs/odbx.science/Remote%20validator?logo=github)](https://github.com/ml-evs/odbx.science/actions?query=branch%3Amaster+)
[![Website](https://img.shields.io/website?down_color=lightgrey&down_message=down&label=OPTIMADE%20API&logo=json&up_color=green&up_message=up&url=https%3A%2F%2Foptimade.odbx.science)](https://optimade.odbx.science/)

This repo contains some notes about the server running at odbx.science. 

This implementation of an OPTIMADE server builds upon the reference server in
the following way:

- Additional routes from `odbx.science/<endpoint>` that mimic `optimade.odbx.science/<endpoint>` but
  provides rich HTML displays of the data.

## Hardware 

As of 02/12/19, the server runs as an RCS OpenStack VM (quadcore Haswell, 8 GB RAM), with three virutal disks attached:

- `/dev/vda`, 80 GB, mounted at `/` contains OS and apps
- `/dev/vdb`, 1 TB, mounted at `/data/sql`, contains SQL database for OQMD
- `/dev/vdc`, 500 GB, mounted at `/data/mongo`, contains our MongoDB.

## Services & security

The site now runs as 5 coupled docker containers, with shared `/tmp/` volume, deployed and built with `docker-compose`:
- `mongo` runs a near-default MongoDB.
- `odbx` runs `gunicorn` that connects to the mongo via `/tmp/mongodb-27017.sock` and serves the HTML responses. (As of 26/04/20, this server also runs the JSON API temporarily at `odbx.science/optimade`.
- `odbx_rest` runs `gunicorn` that connects to the mongo via `/tmp/mongodb-27017.sock` and serves the REST API as JSON at `optimade.odbx.science`.
- `nginx` runs `nginx` that takes HTTP/HTTPS requests and forwards them onto `gunicorn` via the appropriate socket, as well as hosting static content from `./odbx/static/`
- `certbot` calls certbot to attempt to renew SSL certificates every 12 hours.

## Domains & SSL

- The domain `odbx.science` was purchased until 2023 from Namecheap, which currently redirects to the public IP of the VM.
- All `*@odbx.science` email addresses currently redirect to my personal account.
- The domain came with a 1 year SSL certificate (~£4 year after). Since 26/04/20 certbot has been used to get free SSL from Let's Encrypt. This should renew automatically (see notes about `certbot`).
