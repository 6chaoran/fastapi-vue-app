FROM tiangolo/uvicorn-gunicorn:python3.9

LABEL maintainer="Liu Chaoran <6chaoran@gmail.com>"

COPY requirements.txt /tmp/requirements.txt

COPY api.py ./app/main.py
COPY utils.py app.html ./app/
COPY ./saved_model ./app/saved_model
RUN pip install --no-cache-dir -r /tmp/requirements.txt