FROM python:3.11

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x docker/*.sh

RUN alembic upgrade head


#WORKDIR /shorturl

#CMD gunicorn main:app --workers 1 --worker-class uvicorn.workers.UnicornWorker --bind=0.0.0.0:8000
CMD uvicorn main:app --host 0.0.0.0 --port 8000 --workers 1