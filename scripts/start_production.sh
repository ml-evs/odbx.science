#!/bin/bash
mkdir -p logs
mkdir -p /tmp
gunicorn \
    -w 2 \
    -k uvicorn.workers.UvicornWorker \
    --error-logfile logs/odbx_error.log \
    --access-logfile logs/odbx_access.log \
    --capture-output \
    --access-logformat "%(t)s: %(h)s %(l)s %(u)s %(r)s %(s)s %(b)s %(f)s %(a)s" \
    -b unix:/tmp/gunicorn.sock odbx.main:app &

tail -f -n 20 logs/odbx_access.log logs/odbx_error.log
