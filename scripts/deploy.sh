export $(grep -v '^#' creds.env | xargs -d '\n')
docker stop last_gas 
docker rm last_gas 
docker rmi $(docker images -a -q)
docker pull joaomoraes/last-gas
docker run -d -e TOKEN --name last_gas joaomoraes/last-gas 
