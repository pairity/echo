
from logzero import logger
import grpc
from pairity.echo.v1 import (  # type: ignore
    echo_api_pb2 as echo_api,
    echo_api_pb2_grpc as echo_grpc
)    

from src import config

def do_echo(request: echo_api.EchoRequest, loops: int, proc_num: int) -> echo_api.EchoResponse:
    logger.info('Process %d: echoing', proc_num)
    to_echo = request.something
    if loops:
        resp = do_echo(request, loops - 1, proc_num)
        # resp = _echo.Echo(echo_api.EchoRequest(something=to_echo), metadata=list(metadata.items()))
        to_echo += resp.something
    resp = echo_api.EchoResponse(something=to_echo)
    return resp
