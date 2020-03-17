# odbx.science

[![OPTIMADE](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Materials-Consortia/optimade-python-tools/master/.ci/optimade-version.json&logo=json)](https://github.com/Materials-Consortia/OPTIMADE/) 
[![Build Status](https://img.shields.io/github/workflow/status/ml-evs/odbx.science/Remote%20validator?logo=github)](https://github.com/ml-evs/odbx.science/actions?query=branch%3Amaster+)
[![Website](https://img.shields.io/website?down_color=lightgrey&down_message=down&label=OPTIMADE%20API&logo=json&up_color=green&up_message=up&url=https%3A%2F%2Fodbx.science%2Foptimade)](https://odbx.science/optimade)

This repo contains some notes about the server running at odbx.science. 

This implementation of an OPTIMADE server builds upon the reference server in
the following way:

- Additional routes from `odbx.science/<endpoint>` that mimic `odbx.science/optimade/<endpoint>` but
  provides rich HTML displays of the data.

## Hardware 

As of 02/12/19, the server runs as an RCS OpenStack VM (quadcore Haswell, 8 GB RAM), with three virutal disks attached:

- `/dev/vda`, 80 GB, mounted at `/` contains OS and apps
- `/dev/vdb`, 1 TB, mounted at `/data/sql`, contains SQL database for OQMD
- `/dev/vdc`, 500 GB, mounted at `/data/mongo`, contains our MongoDB.

## Services & security

The site now runs as 3 coupled docker containers, with shared `/tmp/` volume, deployed and built with `docker-compose`:
- `odbxscience_mongo` runs a near-default MongoDB.
- `odbxscienc_odbx` runs `gunicorn` that connects to the mongo via `/tmp/mongodb-27017.sock` and serves the JSON and HTML responses.
- `odbxscience_nginx` runs `nginx` that takes HTTP/HTTPS requests and forwards them onto `gunicorn` via `/tmp/gunicorn.sock`, as well as hosting static content.

## Domains & SSL

- The domain `odbx.science` was purchased until 2023 from Namecheap, which currently redirects to the public IP of the VM.
- All `*@odbx.science` email addresses currently redirect to my personal account.
- The domain came with a 1 year SSL certificate (~£4 year after), but free alternatives exists (consider e.g. `cert-bot`).

SSL is currently provided by PositiveSSL via Namecheap. To complete the SSL chain from the certificates provided, I had to follow some of the instructions in the [docs](http://nginx.org/en/docs/http/configuring_https_servers.html#chains).
