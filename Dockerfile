FROM python:3-slim AS builder

ADD . /app
WORKDIR /app
RUN pip install --target=/app -r requirements.txt

FROM python:3-slim
COPY --from=builder /app /app
WORKDIR /app
ENV PYTHONPATH /app

ENTRYPOINT [ "python3","main.py" ]