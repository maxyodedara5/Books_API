# Local machine commands 

uvicorn main:app --reload --env-file ../.env

# Docker Commands 

## Bringing up the containers 

docker compose -f docker-compose-dev.yml --env-file .env-docker up -d

## Tearing down the containers 

docker compose -f docker-compose-dev.yml --env-file .env-docker down