FROM python:3.10.4

# Install make
RUN apt-get install -y make;


# Set up API
WORKDIR last_gas/
COPY . .
RUN make requirements
ENTRYPOINT ["python", "-m", "last_gas"]
