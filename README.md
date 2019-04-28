# Pairity Echo

This is a service that simple echo's the contents of your request. Just use it to test and muck about with the Pairity GRCP server interface.

This project includes both an example of standing up a secure server, as well as connect to a secure server. In order to run this service, you must do two things:

1. Stand up a [Vault-Consul backend](https://gitlab.com/pairity/docker-general/tree/vault-consul/vault-consul) to supply certificates
2. You need to add the following line to `/etc/hosts` (I know...): `127.0.0.1   echo` 

Once these steps are complete, you can start the server and run the client
