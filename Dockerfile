FROM python:3-slim AS builder

ADD . /app
WORKDIR /app
RUN pip install --target=/app -r requirements.txt

FROM grc.io/distroless/python3-debian10
COPY --from=builder /app /app
WORKDIR /app
ENV PYTHONPATH /app

CMD ["main.py"]