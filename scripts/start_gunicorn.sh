#!/bin/bash
mkdir -p logs
gunicorn \
    -w 4 \
    -k uvicorn.workers.UvicornWorker \
    -b 0.0.0.0:5000 \
    --forwarded-allow-ips="*" \
    --error-logfile logs/error.log \
    --access-logfile logs/access.log \
    odbx.main:app;
