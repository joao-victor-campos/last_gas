FROM python:3.10.4

# Install make
RUN apt-get install -y make;

# Install make
RUN apt-get install -y make;

# Install Postgres
RUN sudo apt update;
RUN sudo apt install postgresql postgresql-contrib;


# Set up API
WORKDIR last_gas/
COPY . .
RUN make requirements
ENTRYPOINT ["python", "-m", "last_gas"]
