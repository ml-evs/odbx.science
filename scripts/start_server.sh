#!/bin/bash
source activate optimade
uvicorn optimade.server.main:app --port 8080 --host 0.0.0.0 --workers 2 --access-log
