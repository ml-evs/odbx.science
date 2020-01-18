#!/bin/zsh
source activate odbx 
mkdir -p logs
gunicorn \
    -w 4 \
    -k uvicorn.workers.UvicornWorker \
    -b 0.0.0.0:8080 \
    --error-logfile logs/error.log \
    --access-logfile logs/access.log odbx.main:app;
