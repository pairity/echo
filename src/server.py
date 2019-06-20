"""Simple Echo Service for testing GRPC servers."""

import multiprocessing as mp
import socket
import time
import datetime as dt
from concurrent import futures
import sys
import contextlib

import grpc
from logzero import logger
from pairity.echo.v1 import echo_api_pb2 as echo_api
from pairity.echo.v1 import echo_api_pb2_grpc as echo_grpc  # type: ignore
from pairity.utils.grpc_server import serve
from pairity.utils.jwt import JwtVerifier

from src import logic

_ONE_DAY = dt.timedelta(days=1)
_PROCESS_COUNT = mp.cpu_count()
_THREAD_CONCURRENCY = _PROCESS_COUNT
_RECURSES = 20

class EchoAPIServicer(echo_grpc.EchoAPIServicer):
    """Just echo requests."""

    def __init__(self, proc_num: int):
        self.proc_num = proc_num

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
        resp = echo_api.EchoResponse()
        # This is in a separate module so that we can quickly test out an internal worker pool
        resp = logic.do_echo(request, _RECURSES, self.proc_num)
        return resp

def _wait_forever(server):
    try:
        while True:
            time.sleep(_ONE_DAY.total_seconds())
    except KeyboardInterrupt:
        logger.warning('Shutting down now')
        server.stop(grace=None)

def _run_server(bind_address, proc_num):

    logger.info('Starting a new server...')
    options = (('grpc.so_reuseport', 1),)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=_THREAD_CONCURRENCY), options=options)
    echo_grpc.add_EchoAPIServicer_to_server(EchoAPIServicer(proc_num), server)
    server.add_insecure_port(bind_address)
    server.start()
    logger.info('Server started...')
    _wait_forever(server)

@contextlib.contextmanager
def _reserve_port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT) != 1:
        raise RuntimeError('Failed to set SO_REUSEPORT.')
    sock.bind(('', 50051))
    try:
        yield sock.getsockname()[1]
    finally:
        sock.close()

def main():
    with _reserve_port() as port:
        bind_address = '127.0.0.1:{}'.format(port)
        logger.info("Binding to '%s'", bind_address)
        if len(sys.argv) > 1 and sys.argv[1] == '--single':
            _run_server(bind_address, 0)
        else:
            workers = []
            for proc_num in range(_PROCESS_COUNT):
                # NOTE: It is imperative that the worker subprocesses be forked before
                # any gRPC servers start up. See
                # https://github.com/grpc/grpc/issues/16001 for more details.
                worker = mp.Process(
                    target=_run_server, args=(bind_address, proc_num))
                worker.start()
                workers.append(worker)
            try:
                for worker in workers:
                    worker.join()
                    workers.pop(0)
            except KeyboardInterrupt:
                logger.warning('Caught ctrl-c. Stopping workers.')
                for worker in workers:
                    worker.kill()
                    worker.join()
                    logger.info('Worker stopped.')
                logger.warning('Exiting...')

if __name__ == '__main__':
    main()
