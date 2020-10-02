#!/bin/bash
mkdir -p logs
mkdir -p /tmp

touch logs/odbx_rest_test_access.log
touch logs/odbx_rest_test_error.log

tail -f -n 20 logs/odbx_rest_test_access.log logs/odbx_rest_test_error.log &

gunicorn \
    -w 2 \
    -k uvicorn.workers.UvicornWorker \
    --error-logfile logs/odbx_rest_test_error.log \
    --access-logfile logs/odbx_rest_test_access.log \
    --access-logformat "%(t)s: %(h)s %(l)s %(u)s %(r)s %(s)s %(b)s %(f)s %(a)s" \
    -b unix:/tmp/gunicorn_rest_test.sock odbx.main_rest:app
