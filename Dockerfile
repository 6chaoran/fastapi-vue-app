FROM tiangolo/uvicorn-gunicorn:python3.9-slim

LABEL maintainer="Liu Chaoran <6chaoran@gmail.com>"

COPY docker_requirements.txt /tmp/requirements.txt

COPY api.py ./app/main.py
COPY utils.py app.html ./app/
COPY ./saved_model ./app/saved_model
RUN pip install --no-cache-dir -r /tmp/requirements.txt
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
