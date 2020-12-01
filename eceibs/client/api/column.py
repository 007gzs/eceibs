# encoding: utf-8

from .base import CecibsBaseAPI


class Column(CecibsBaseAPI):
    """
    专栏－视频接口
    """
    def column_list(self, _type=1):
        """
        专栏列表接口

        :param _type: 类型 (1:视频)
        """
        return self._post(
            '/v1/column/list', {'type': _type, 'company_code': self.company_code}, result_processor=lambda x: x['list']
        )

    def file_media(self, _id, login_name):
        """
        视频播放－获取m3u8接口

        :param _id: 视频文件id
        :param login_name: 当前登陆的用户名称
        :return: m3u8 url
        """
        return self._gen_url(
            '/v1/file/media',
            {'company_code': self.company_code, 'id': _id, 'login_name': login_name},
            token_key='token'
        )
