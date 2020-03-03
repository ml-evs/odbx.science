#!/bin/bash
mkdir -p logs
mkdir -p /tmp
gunicorn \
    -w 1 \
    -k uvicorn.workers.UvicornWorker \
    --error-logfile logs/odbx_error.log \
    --access-logfile logs/odbx_access.log \
    --capture-output \
    --access-logformat "%(t)s: %(h)s %(l)s %(u)s %(r)s %(s)s %(b)s %(f)s %(a)s" \
    -b unix:/tmp/gunicorn.sock odbx.main:app;
