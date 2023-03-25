export $(grep -v '^#' creds.env | xargs -d '\n')
docker stop last_gas 
docker rm last_gas 
docker rmi $(docker images -a -q)
docker pull joaomoraes/last-gas:latest
docker run --restart unless-stopped -d -e TOKEN --name last_gas joaomoraes/last-gas:latest
