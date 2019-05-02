"""Simple Echo Service for testing GRPC servers."""

from pairity.echo.v1 import echo_api_pb2_grpc as echo_grpc, echo_api_pb2 as echo_api #type: ignore
from pairity.utils.grpc_server import serve, config
from pairity.utils.jwt import JwtVerifier

import grpc

if __name__ == '__main__':
    serve()

class EchoAPIServicer(echo_grpc.EchoAPIServicer):
    """Just echo requests."""
    VERIFIER = JwtVerifier(config.cognito.user_pool_id, config.aws.region)


    @VERIFIER.require_jwt
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
        to_echo = request.something
        resp = echo_api.EchoResponse(something=to_echo)
        return resp

