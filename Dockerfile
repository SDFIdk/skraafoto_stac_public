FROM python:3.8-slim as production

# Any python libraries that require system libraries to be installed will likely
# need the following packages in order to build
RUN apt-get update \
    && apt-get install -y build-essential postgresql-client \
    && rm -rf /var/lib/{apt,dpkg,cache,log}/

ARG install_dev_dependencies=true

WORKDIR /app

# Install stac_fastapi.types
COPY src /app

ENV PATH=$PATH:/install/bin

RUN mkdir -p /install && \
    pip install -e ./stac_fastapi/types && \
    pip install -e ./stac_fastapi/api && \
    pip install -e ./stac_fastapi/extensions && \
    pip install -e ./stac_fastapi/sqlalchemy[server]

CMD ["python","-m","uvicorn","--proxy-headers","stac_fastapi.sqlalchemy.app:app","--host","0.0.0.0","--port","8081"]
