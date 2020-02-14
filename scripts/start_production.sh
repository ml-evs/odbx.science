#!/bin/bash
mkdir -p logs
mkdir -p /tmp
gunicorn \
    -w 1 \
    -k uvicorn.workers.UvicornWorker \
    --error-logfile logs/error.log \
    --access-logfile logs/access.log \
    -b unix:/tmp/gunicorn.sock odbx.main:app;
