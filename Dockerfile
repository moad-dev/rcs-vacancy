FROM python:3.11-slim as wheel-builder

RUN apt-get update && \
    apt-get install --no-install-recommends -y build-essential gcc
    
COPY requirements.txt /tmp/requirements.txt
# RUN pip wheel --wheel-dir=/root/.cache/pip/wheels --only-binary ':all:' -r /tmp/requirements.txt
RUN pip wheel --wheel-dir=/root/.cache/pip/wheels -r /tmp/requirements.txt


FROM python:3.11-slim
WORKDIR /app


COPY requirements.txt ./
COPY --from=wheel-builder /root/.cache/pip/wheels /root/.cache/pip/wheels
RUN pip install --no-index --find-links=/root/.cache/pip/wheels -r requirements.txt


COPY app.py ./

CMD uvicorn app:app --host 0.0.0.0 --port ${AI_PORT} --log-level warning
