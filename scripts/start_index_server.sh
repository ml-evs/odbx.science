#!/bin/bash
mkdir -p logs
mkdir -p /tmp

touch logs/odbx_index_error.log
touch logs/odbx_index_access.log

tail -f -n 20 logs/odbx_index_error.log logs/odbx_index_access.log &

gunicorn \
    -w 2 \
    -k uvicorn.workers.UvicornWorker \
    --error-logfile logs/odbx_index_error.log \
    --access-logfile logs/odbx_index_access.log \
    --access-logformat "%(t)s: %(h)s %(l)s %(u)s %(r)s %(s)s %(b)s %(f)s %(a)s" \
    -b unix:/tmp/gunicorn_index.sock odbx.main_index:app
