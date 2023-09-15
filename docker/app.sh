##!/bin/bash
#
#alembic upgrade head
#
#cd short_url
#
##gunicorn main:app --workers 4 --worker-class uvicorn.workers.UnicornWorker --bind=0.0.0.0:8000
#uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4