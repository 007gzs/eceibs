# encoding: utf-8

import logging

from . import api
from .base import BaseClient
from ..storage.cache import EceibsCache

logger = logging.getLogger(__name__)


class EceibsClient(BaseClient):
    auth = api.Auth()
    open = api.Open()
    column = api.Column()

    def __init__(self, company_code, open_secret, storage=None, timeout=None):
        super().__init__(storage=storage, timeout=timeout)
        self.company_code = company_code
        self.open_secret = open_secret
        self.cache = EceibsCache(self.storage)

    def _handle_pre_request(self, method, uri, kwargs):
        if kwargs is None:
            kwargs = dict()
        kwargs.setdefault("headers", dict())
        if 'Authorization' in kwargs['headers']:
            raise ValueError("headers中不允许有 Authorization: " + kwargs['headers']['Authorization'])
        kwargs['headers']['Authorization'] = "Bearer " + self.access_token
        return method, uri, kwargs

    def _handle_request_except(self, e, func, *args, **kwargs):
        # if e.errcode in (33001, 40001, 42001, 40014):
        #     self.cache.access_token.delete()
        #     if self.auto_retry:
        #         return func(*args, **kwargs)

        raise e

    @property
    def access_token(self):
        self.cache.access_token.get()
        token = self.cache.access_token.get()
        if token is None:
            token = self.get_access_token()
            self.cache.access_token.set(value=token, ttl=120)
        return token

    def get_access_token(self):
        return self._request(
            'POST',
            '/v1/auth/login',
            data={'code': self.company_code, 'open_secret': self.open_secret},
            result_processor=lambda x: x['access_token']
        )


class TestEceibsClient(EceibsClient):
    def __init__(self, company_code="apidemo", open_secret=None, storage=None, timeout=None):
        super().__init__(company_code=company_code, open_secret=open_secret, storage=storage, timeout=timeout)

    def get_access_token(self):
        return self._request(
            'GET',
            'http://samples.eceibs.com.cn/apidemo/api/auth.php',
            result_processor=lambda x: x['access_token']
        )
