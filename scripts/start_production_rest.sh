#!/bin/bash
mkdir -p logs
mkdir -p /tmp
gunicorn \
    -w 2 \
    -k uvicorn.workers.UvicornWorker \
    --error-logfile logs/odbx_rest_error.log \
    --access-logfile logs/odbx_rest_access.log \
    --capture-output \
    --access-logformat "%(t)s: %(h)s %(l)s %(u)s %(r)s %(s)s %(b)s %(f)s %(a)s" \
    -b unix:/tmp/gunicorn_rest.sock odbx.main_rest:app &

tail -f -n 20 logs/odbx_rest_access.log logs/odbx_rest_error.log
