FROM python:3.8-slim as production

# Any python libraries that require system libraries to be installed will likely
# need the following packages in order to build
RUN apt-get update \
    && apt-get install -y build-essential postgresql-client \
    && apt-get upgrade -y \
    && rm -rf /var/lib/{apt,dpkg,cache,log}/

WORKDIR /app

# Install stac_fastapi.types
COPY src /app

ENV PATH=$PATH:/install/bin

RUN mkdir -p /install && \
    pip install -U pip \
    pip install -e ./stac_fastapi/types && \
    pip install -e ./stac_fastapi/api && \
    pip install -e ./stac_fastapi/extensions && \
    pip install -e ./stac_fastapi/sqlalchemy[server]

CMD ["python","-m","uvicorn","--proxy-headers","stac_fastapi.sqlalchemy.app:app","--host","0.0.0.0","--port","8081","--timeout-keep-alive","65"]
