export $(grep -v '^#' creds.env | xargs -d '\n')
docker stop last_gas-prod
docker rm last_gas-prod 
docker rmi $(docker images -a -q last_gas:latest)
docker pull joaomoraes/last-gas:latest
docker run --restart unless-stopped -d -e TOKEN --name last_gas-prod joaomoraes/last-gas:latest
