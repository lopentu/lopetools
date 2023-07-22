#!/usr/bin/env sh

uvicorn api.main:app --reload --port 8003 --host 0.0.0.0
