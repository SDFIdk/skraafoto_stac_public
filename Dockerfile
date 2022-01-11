FROM python:3.8-slim as production

# Any python libraries that require system libraries to be installed will likely
# need the following packages in order to build
RUN apt-get update \
    && apt-get install -y build-essential \
    && rm -rf /var/lib/{apt,dpkg,cache,log}/

ENV CURL_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt

ARG install_dev_dependencies=true

WORKDIR /app

# Install stac_fastapi.types
COPY src /app

ENV PATH=$PATH:/install/bin

RUN mkdir -p /install && \
    pip install -e ./stac_fastapi/types[dev] && \
    pip install -e ./stac_fastapi/api[dev] && \
    pip install -e ./stac_fastapi/extensions[dev] && \
    pip install -e ./stac_fastapi/sqlalchemy[dev,server]
