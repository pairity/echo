from pairity.echo.v1 import echo_api_pb2 as echo_api, echo_api_pb2_grpc as echo_grpc
import grpc
import time
import multiprocessing as mp
from logzero import logger

REQUESTS = 10000


def _make_requests(worker_idx: int = 0):
    try:
        channel = grpc.insecure_channel('127.0.0.1:50051')
        stub = echo_grpc.EchoAPIStub(channel)
        request = echo_api.EchoRequest(something='anything')
        start = time.time()
        futures = []
        logger.info('Worker %d: Making requests', worker_idx)
        for _ in range(REQUESTS):
            futures.append(stub.Echo.future(request))
        logger.info('Worker %d: Requests made', worker_idx)
        logger.info('Worker %d: Waiting for results', worker_idx)

        for future in futures:
            future.result()

        logger.info('Received results - Returning...')
        logger.info('Took %d to make %d requests', (time.time() - start), REQUESTS)
    except KeyboardInterrupt:
        logger.warning('Worker %d: Stopping...', worker_idx)


def main():

    workers = []
    for worker_idx in range(9):
        worker = mp.Process(target=_make_requests, args=(worker_idx,))
        worker.start()
        workers.append(worker)

    try:
        for worker in workers:
            worker.join()
            workers.pop(0)
    except KeyboardInterrupt:
        logger.warning('Caught ctrl-c. Stopping workers...')
        for worker in workers:
            worker.kill()
            worker.join()


if __name__ == '__main__':
    main()
