# Rfam API

Get a local installation of the Rfam API using [Docker](https://www.docker.com/)
and the public Rfam MySQL database.

## Development

Clone this repository, then start docker:

```
export RFAM_API_HOME=/path/to/this/code
docker-compose up
```

The API should be available at *http://0.0.0.0:4000*.

By default the website connects to the public Rfam database but an alternative
database can be specified in `api/api/local_settings.py` (ignored by git).

## Docker cheat sheet

```
# list running docker containers
docker ps

# login to running container from another terminal
docker exec -it rfam-api bash
```
