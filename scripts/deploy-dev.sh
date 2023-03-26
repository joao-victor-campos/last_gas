export $(grep -v '^#' creds.env | xargs -d '\n')
docker stop last_gas-dev
docker rm last_gas-dev
docker rmi $(docker images -a -q last_gas:dev)
docker pull joaomoraes/last-gas:dev
docker run --restart unless-stopped -d -e TOKEN_DEV --name last_gas-dev joaomoraes/last-gas:dev
