"""Simple Echo Service for testing GRPC servers."""

import multiprocessing as mp

import grpc
from logzero import logger
from pairity.echo.v1 import echo_api_pb2 as echo_api
from pairity.echo.v1 import echo_api_pb2_grpc as echo_grpc  # type: ignore
from pairity.utils.grpc_server import config, serve
from pairity.utils.jwt import JwtVerifier

from echo import logic

POOL = mp.Pool(processes=8)

if __name__ == '__main__':
    serve()



class EchoAPIServicer(echo_grpc.EchoAPIServicer):
    """Just echo requests."""


    def Echo(self, request: echo_api.EchoRequest, context: grpc.RpcContext) -> echo_api.EchoResponse:
        """gRPC linkage for Echo.

        Parameters
        ----------
        request : EchoRequest
            The Echo request
        context : grpc.RpcContext
            The RPC context

        Returns
        -------
        EchoResponse
            The Echo response

        """
        logger.info('Here')
        resp = POOL.apply(logic.do_echo, args=(request.SerializeToString(), dict(context.invocation_metadata())))
        logger.info(resp)
        return resp
