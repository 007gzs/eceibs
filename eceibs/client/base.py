# encoding: utf-8
import inspect
import logging
import requests
from urllib.parse import urljoin, urlencode

from ..core.exceptions import EceibsClientException
from ..core.utils import json_loads
from ..storage.memorystorage import MemoryStorage
from .api.base import CecibsBaseAPI

logger = logging.getLogger(__name__)


def _is_api_endpoint(obj):
    return isinstance(obj, CecibsBaseAPI)


class BaseClient(object):

    _http = requests.Session()

    API_BASE_URL = 'https://openapi.eceibs.net/'

    def __new__(cls, *args, **kwargs):
        self = super(BaseClient, cls).__new__(cls)
        api_endpoints = inspect.getmembers(self, _is_api_endpoint)
        for name, api in api_endpoints:
            api_cls = type(api)
            api = api_cls(self)
            setattr(self, name, api)
        return self

    def __init__(self, storage=None, timeout=None):
        self.storage = storage or MemoryStorage()
        self.timeout = timeout

    def _request(self, method, url_or_endpoint, **kwargs):
        if not url_or_endpoint.startswith(('http://', 'https://')):
            api_base_url = kwargs.pop('api_base_url', self.API_BASE_URL)
            url = urljoin(api_base_url, url_or_endpoint)
        else:
            url = url_or_endpoint

        if 'params' not in kwargs:
            kwargs['params'] = {}
        if isinstance(kwargs.get('data', ''), dict):
            kwargs['data'] = urlencode(kwargs['data'])
            if 'headers' not in kwargs:
                kwargs['headers'] = {}
            kwargs['headers']['Content-Type'] = 'application/x-www-form-urlencoded'

        kwargs['timeout'] = kwargs.get('timeout', self.timeout)
        result_processor = kwargs.pop('result_processor', None)
        res = self._http.request(
            method=method,
            url=url,
            **kwargs
        )
        try:
            res.raise_for_status()
        except requests.RequestException as reqe:
            logger.error("\n【请求地址】: %s\n【请求参数】：%s \n%s\n【异常信息】：%s",
                         url, kwargs.get('params', ''), kwargs.get('data', ''), reqe)
            raise EceibsClientException(
                errcode=None,
                errmsg=None,
                client=self,
                request=reqe.request,
                response=reqe.response
            )

        result = self._handle_result(res, method, url, result_processor, **kwargs)

        logger.debug("\n【请求地址】: %s\n【请求参数】：%s \n%s\n【响应数据】：%s",
                     url, kwargs.get('params', ''), kwargs.get('data', ''), result)
        return result

    def _decode_result(self, res):
        try:
            result = json_loads(res.content.decode('utf-8', 'ignore'), strict=False)
        except (TypeError, ValueError):
            # Return origin response object if we can not decode it as JSON
            logger.debug('Can not decode response as JSON', exc_info=True)
            return res
        return result

    def _handle_result(self, res, method=None, url=None, result_processor=None, **kwargs):
        if not isinstance(res, dict):
            # Dirty hack around asyncio based AsyncWeChatClient
            result = self._decode_result(res)
        else:
            result = res

        if not isinstance(result, dict):
            return result

        if 'success' not in result or not result['success']:
            code = result.get('code', -1)
            msg = result.get('msg', code)

            logger.error("\n【请求地址】: %s\n【请求参数】：%s \n%s\n【错误信息】：%s",
                         url, kwargs.get('params', ''), kwargs.get('data', ''), result)
            raise EceibsClientException(
                code,
                msg,
                client=self,
                request=res.request,
                response=res
            )
        if 'result' in result:
            result = result['result']
        return result if not result_processor else result_processor(result)

    def _handle_pre_request(self, method, uri, kwargs):
        return method, uri, kwargs

    def _handle_request_except(self, e, func, *args, **kwargs):
        raise e

    def request(self, method, uri, **kwargs):
        method, uri_with_access_token, kwargs = self._handle_pre_request(method, uri, kwargs)
        try:
            return self._request(method, uri_with_access_token, **kwargs)
        except EceibsClientException as e:
            return self._handle_request_except(e, self.request, method, uri, **kwargs)

    def get_access_token(self):
        raise NotImplementedError

    @property
    def access_token(self):
        raise NotImplementedError

    def get(self, uri, params=None, **kwargs):
        """
        get 接口请求

        :param uri: 请求url
        :param params: get 参数（dict 格式）
        """
        if params is not None:
            kwargs['params'] = params
        return self.request('GET', uri, **kwargs)

    def post(self, uri, data=None, params=None, **kwargs):
        """
        post 接口请求

        :param uri: 请求url
        :param data: post 数据
        :param params: post接口中url问号后参数（dict 格式）
        """
        if data is not None:
            kwargs['data'] = data
        if params is not None:
            kwargs['params'] = params
        return self.request('POST', uri, **kwargs)

    def gen_url(self, uri, params=None, token_key='access_token', **kwargs):
        """
        生成url

        :param uri: 请求url
        :param params: get 参数（dict 格式）
        :param token_key: token参数
        """
        if params is None:
            params = dict()
        params[token_key] = self.access_token
        if not uri.startswith(('http://', 'https://')):
            api_base_url = kwargs.pop('api_base_url', self.API_BASE_URL)
            url = urljoin(api_base_url, uri)
        else:
            url = uri
        if '?' not in url:
            url += "?"
        if not url.endswith("&"):
            url += "&"
        url += urlencode(params)
        return url
