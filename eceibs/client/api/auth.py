# encoding: utf-8

from .base import CecibsBaseAPI


class Auth(CecibsBaseAPI):
    """
    授权接口
    """
    def verify_open(self):
        """
        授权校验接口
        """
        return self._post('/v1/service/verify_open', result_processor=lambda x: True)
