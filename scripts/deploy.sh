export $(grep -v '^#' creds.env | xargs -d '\n')
docker stop last_gas 
docker rmi $(docker images -a -q)
docker pull joaomoraes/last-gas
docker run joaomoraes/last-gas -d -e TOKEN last_gas 
