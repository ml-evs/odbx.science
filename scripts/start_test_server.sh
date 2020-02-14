#!/bin/bash
uvicorn odbx.main:app --reload --port 5000 --host 0.0.0.0 --workers 2 --access-log
