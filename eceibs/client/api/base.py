# encoding: utf-8


class CecibsBaseAPI(object):

    API_BASE_URL = None

    def __init__(self, client=None):
        self._client = client

    def _get(self, url, params=None, **kwargs):
        if self.API_BASE_URL and 'api_base_url' not in kwargs:
            kwargs['api_base_url'] = self.API_BASE_URL
        return self._client.get(url, params, **kwargs)

    def _post(self, url, data=None, params=None, **kwargs):
        if self.API_BASE_URL and 'api_base_url' not in kwargs:
            kwargs['api_base_url'] = self.API_BASE_URL
        return self._client.post(url, data, params, **kwargs)

    def _gen_url(self, url, params=None, **kwargs):
        if self.API_BASE_URL and 'api_base_url' not in kwargs:
            kwargs['api_base_url'] = self.API_BASE_URL
        return self._client.gen_url(url, params, **kwargs)

    @property
    def company_code(self):
        return self._client.company_code
