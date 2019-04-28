"""An echo client."""

import grpc
import pairity.echo.v1.echo_api_pb2 as echo_api
import pairity.echo.v1.echo_api_pb2_grpc as echo_grpc
from pairity.utils.utils import get_secure_channel

def run():
    """Ask the echo server to echo something."""

    channel = get_secure_channel('echo')
    stub = echo_grpc.EchoAPIStub(channel)
    request = echo_api.EchoRequest(something='Please echo this')
    resp = stub.Echo(request)
    print(resp.something)

if __name__ == '__main__':
    run()
