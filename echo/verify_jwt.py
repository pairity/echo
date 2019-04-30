"""Verify JWT tokens with Cognito keys"""

import json
import os
from functools import wraps
from typing import Any, Callable

import grpc
import requests
from jwcrypto import jwk, jwt
from jwcrypto.common import JWException
from logzero import logger
from pairity.utils import set_context
from pairity.v1 import status_pb2 as status

TOKEN_HEADER = 'pairity-auth-token'

#pylint: disable=invalid-name
logger.info('Getting Public Keys for auth')
_region = os.environ['AWS_DEFAULT_REGION']
_user_pool_id = os.environ['COGNITO_USER_POOL_ID']
_resp = requests.get(
    F'https://cognito-idp.{_region}.amazonaws.com/{_user_pool_id}/.well-known/jwks.json'
).content.decode()
KEYS = jwk.JWKSet()
KEYS.import_keyset(_resp)


def require_jwt(a_function: Callable) -> Callable:
    """A decorator to require JWT for a particular function.Callable

    Parameters
    ----------
    a_function : Callable
        The function to decorate

    Returns
    -------
    Callable
        The decorated function

    """

    @wraps(a_function)
    def _wrapper(caller: Callable, request: Any, context: grpc.RpcContext) -> Any:
        metadata = dict(context.invocation_metadata())
        logger.warn(metadata)
        if not TOKEN_HEADER in metadata:
            set_context(
                context, status.STATUS_UNAUTHENTICATED,
                F'Authentication is required for {a_function.__name__}'
            )
        token = metadata[TOKEN_HEADER]

        try:
            _jwt = jwt.JWT(jwt=token, key=KEYS)
        except JWException as e:
            set_context(context, status.STATUS_INVALID_ARGUMENT, str(e))

        resp = a_function(caller, request, context)
        return resp

    return _wrapper
