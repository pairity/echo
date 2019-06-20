# Pairity Echo

This is no an expermental server, the start of Contrail.

To build the image: `docker build . -t echo --build-arg FURY_AUTH=$FURY_AUTH`
To run the image: `docker run --name echo-service --rm echo python -m src.server`
TO run the image with a single process: `docker run --name echo-service --rm echo python -m src.server --single`

I have not been able to connect to this from outside of the docker container. My assumption is some socket weirdness because we are reliant on `SO_REUSEPORT` which I haven't been able to
successfully set that option on MacOS. Any thoughts are welcome.

There is an included client that will use 9 workers to make 10,000 requests each to the server and record how long each process takes and how long the whole process takes. 
To run the client: `docker exec -it echo-service python client.py`
