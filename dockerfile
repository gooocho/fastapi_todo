FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /app

COPY app/requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt
