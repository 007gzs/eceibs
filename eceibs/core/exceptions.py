# encoding: utf-8

from .utils import to_binary, to_text


class EceibsException(Exception):

    def __init__(self, errcode, errmsg):
        """
        :param errcode: Error code
        :param errmsg: Error message
        """
        self.errcode = errcode
        self.errmsg = errmsg

    def __str__(self):
        return 'Error code: {code}, message: {msg}'.format(code=self.errcode, msg=self.errmsg)

    def __repr__(self):
        return '{klass}({code}, {msg})'.format(
            klass=self.__class__.__name__,
            code=self.errcode,
            msg=self.errmsg
        )


class EceibsClientException(EceibsException):
    """WeChat API client exception class"""
    def __init__(self, errcode, errmsg, client=None,
                 request=None, response=None):
        super().__init__(errcode, errmsg)
        self.client = client
        self.request = request
        self.response = response


class InvalidSignatureException(EceibsException):
    """Invalid signature exception class"""

    def __init__(self, errcode=-40001, errmsg='Invalid signature'):
        super(InvalidSignatureException, self).__init__(errcode, errmsg)


class InvalidCorpIdOrSuiteKeyException(EceibsException):
    """Invalid app_id exception class"""

    def __init__(self, errcode=-40005, errmsg='Invalid CorpIdOrSuiteKey'):
        super(InvalidCorpIdOrSuiteKeyException, self).__init__(errcode, errmsg)
