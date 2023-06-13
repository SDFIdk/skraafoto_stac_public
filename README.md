# stac-api 📚🗄️

## skraafotodistribution-stac-api

SDFI implementation of STAC API.

Original code:
```
MIT License
Copyright (c) 2020 Arturo AI
```

# Dokumentation
En lynintroduktion findes under [How To Get Started](./dokumentation.md/#how-to-get-started). Mere uddybende dokumentation findes i [./dokumentation.md](./dokumentation.md)

---

## Configuration

### Update 2023.06.13
Python image locked to version 3.18.5 as higher versionen introduces a bug with pip where egg files isn't created linking to stac_fastapi dev install


The application is configured using environment variables. These may be put in a file `/.env` like

```.env
WEB_CONCURRENCY=10
DEBUG=TRUE
POSTGRES_USER=my_user
POSTGRES_PASS=my_password
POSTGRES_DBNAME=database_name
POSTGRES_HOST=database_host
POSTGRES_PORT=5432
POSTGRES_APPLICATION_NAME=my_debug_application
# Base path of the proxying tile server
COGTILER_BASEPATH=https://skraafotodistribution-tile-api.k8s-test-121.septima.dk/cogtiler
```

## Development

### Running with docker compose

To run it simply add your configuration in an `.env` file as described above and use:
`docker compose build`
`docker compose up`

Now you can look at the api at http://localhost:8081/.

### Running with docker compose
Remember to attach debugger Python: Remote Attach

### Debugging with docker

Using vscode install the [Docker](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker) extension.

Then create

`.vscode/launch.json`:

```json
{
  // Use IntelliSense to learn about possible attributes.
  // Hover to view descriptions of existing attributes.
  // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Docker: Python - Fastapi",
      "type": "docker",
      "request": "launch",
      "preLaunchTask": "docker-run: debug",
      "python": {
        "pathMappings": [
          {
            "localRoot": "${workspaceFolder}/src/stac_fastapi",
            "remoteRoot": "/app/stac_fastapi"
          }
        ],
        "projectType": "fastapi"
      }
    }
  ]
}
```

and `.vscode/tasks.json` (note that app configuration cannot be read from the `.env` file here and needs to be repeated):

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "type": "docker-build",
      "label": "docker-build",
      "platform": "python",
      "dockerBuild": {
        "tag": "skraafoto_stac_public:latest",
        "dockerfile": "${workspaceFolder}/Dockerfile_dev",
        "context": "${workspaceFolder}",
        "pull": true
      }
    },
    {
      "type": "docker-run",
      "label": "docker-run: debug",
      "dependsOn": ["docker-build"],
      "dockerRun": {
        "ports": [
          {
            "containerPort": 8081,
            "hostPort": 8081
          }
        ],
        "env": {
          "APP_PORT": "8081",
          "DEBUG": "TRUE",
          "ENVIRONMENT": "local",
          "POSTGRES_USER": "my_db_user",
          "POSTGRES_PASS": "my_db_password",
          "POSTGRES_DBNAME": "db_name",
          "POSTGRES_HOST": "db_host",
          "POSTGRES_PORT": "db_port",
          "POSTGRES_APPLICATION_NAME": "stac_fastapi_vscode_debugging",
          "WEB_CONCURRENCY": "1",
          "COGTILER_BASEPATH": "https://skraafotodistribution-tile-api.k8s-test-121.septima.dk/cogtiler"
        }
      },
      "python": {
        "args": [
          "stac_fastapi.sqlalchemy.app:app",
          "--host",
          "0.0.0.0",
          "--port",
          "8081",
          "--reload"
        ],
        "module": "uvicorn"
      }
    }
  ]
}
```

Now you should be able to hit "Start debugging" `Docker: Python - Fastapi` which will launch the API in a docker container supporting breakpoints in your code.

### Testing

Pytest use the configuration from the `.env`.
Pytest requires the modules to be installed in editable mode. To do this correctly, we use Anaconda.

`conda create --name skraafoto-stac-api python=3.9`

On my machine it was also needed to run:

`conda bash init`

Now activate the environment:

`conda activate skraafoto-stac-api`

Go to the projects folder in the environment.

Install the packages in this order:

```
  pip install wheel && \
  pip install -e "./src/stac_fastapi/api[dev]" && \
  pip install -e "./src/stac_fastapi/types[dev]" && \
  pip install -e "./src/stac_fastapi/extensions[dev]"
```

Now install the SQLalchemy implementation:

`pip install -e "./src/stac_fastapi/sqlalchemy[dev,server]"`

And finally you should be able to run `pytest src` on the commandline, and have VScode discover the tests using the `testing` icon in the left-hand toolbar (it looks like a chemestry vial). Make sure VScode has the proper python interpreter configured, it should be something like `~\anaconda3\envs\skraafoto-stac-api\python.exe` or `~\Miniconda3\envs\skraafoto-stac-api\python.exe`. It can be set typing `CTRL + SHIFT + P` -> `Python: Select interpreter` and then finding the new interpreter. If you can't find it, you need to reload VSCode.

You can also now debug the test methods from VSCode.
If you get an error saying `ImportError: DLL load failed while importing _sqlite3` when trying to debug the test methods, check the DDLs folder from the `skraafoto-stac-api` env `C:\Users\YOURUSER\{Anaconda3 or Miniconda3}\envs\skraafoto-stac-api\DLLs` if it is missing the `sqlite3.ddl` file. If it is missing download the sqlite3 dll from https://www.sqlite.org/download.html under `Precompiled Binaries for Windows` (find your system version), place it in the 
folder `C:\Users\YOURUSER\{Anaconda3 or Miniconda3}\envs\skraafoto-stac-api\DLLs` and restart your VSCode.

### Self-contained test

SKRAAFOTO_STAC_PUBLIC requires a database, populated with data, to run the tests against. To run a completely self-contained test, a docker-compose file named `docker-compose.unittest.yml` is made available.

Run the test compose file `docker-compose -f .\docker-compose.unittest.yml up`. The docker compose file spins up a database, and populates it with data using an alembic migration file. The tests are then run using pytest against the API and a report is generated at `/app/report` in the root directory and is mounted out to `./docker/reports`. Any changes made to the database, has to be mirrored by creating a new alembic version. For more information see https://alembic.sqlalchemy.org/en/latest/tutorial.html

