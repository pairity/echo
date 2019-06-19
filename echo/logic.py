
from logzero import logger
import grpc
from pairity.echo.v1 import (  # type: ignore
    echo_api_pb2 as echo_api,
    echo_api_pb2_grpc as echo_grpc
)    

RECURSES = 20

def do_echo(request: echo_api.EchoRequest, metadata) -> echo_api.EchoResponse:
    _echo = echo_grpc.EchoAPIStub(grpc.insecure_channel('localhost:50051'))
    repeats = int(metadata.get('repeats', '1'))
    logger.info('On repeat %d', repeats)
    metadata['repeats'] = str(int(metadata.get('repeats', '1')) + 1)
    to_echo = request.something
    if repeats != RECURSES:
        resp = _echo.Echo(echo_api.EchoRequest(something=to_echo), metadata=list(metadata.items()))
        to_echo += resp.something
    resp = echo_api.EchoResponse(something=to_echo)
    return resp.SerializeToString().decode()
