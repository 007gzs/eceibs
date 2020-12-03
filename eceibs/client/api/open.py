# encoding: utf-8
import json

from optionaldict import optionaldict

from .base import CecibsBaseAPI


class Open(CecibsBaseAPI):
    """
    在线课程学课/考试接口
    """
    def lesson_list_open(self, trainplan_id=None, res_type=None):
        """
        课程清单接口

        :param trainplan_id: 计划id
        :param res_type: 默认返回全部类型资源，支持传入指定类型资源：lesson:在线课程;paper:试卷;document:拓展阅读
        :return:
        """
        assert res_type in (None, "lesson", "paper", "document")
        return self._post(
            '/v1/open/lesson_list_open',
            optionaldict({
                'company_code': self.company_code,
                'trainplan_id': trainplan_id,
                'res_type': res_type
            })
        )

    def _gen_page(
        self,
        uri,
        _from,
        trainplan_id,
        resources_id,
        login_name,
        hide_top_bar=0,
        back_url=None,
        show_full_screen_btn=0,
        show_speed_btn=0,
        disable_drag=0
    ):
        """
        生成页面

        :param uri: 接口uri
        :param _from: 平台类型，1：手机端; 2:PC端
        :param trainplan_id: 计划ID
        :param resources_id: 课程ID
        :param login_name: 当前登录的用户名称
        :param hide_top_bar: 是否隐藏顶部菜单栏
        :param back_url: 返回按钮的链接地址
        :param show_full_screen_btn: h5学课是否显示全屏按钮
        :param show_speed_btn: 是否显示倍速
        :param disable_drag: 是否禁止进度条拖拽
        :return: url
        """
        assert _from in (1, 2)
        params = optionaldict({
            "from": _from,
            "code": self.company_code,
            "trainplan_id": trainplan_id,
            "resources_id": resources_id,
            "login_name": login_name,
            "hide_top_bar": 1 if hide_top_bar else 0,
            "back_url": back_url,
            "show_full_screen_btn": 1 if show_full_screen_btn else 0,
            "show_speed_btn": 1 if show_speed_btn else 0,
            "disable_drag": 1 if disable_drag else 0,
        })
        return self._gen_url(uri, params)

    def lesson_open(
            self,
            _from,
            trainplan_id,
            resources_id,
            login_name,
            hide_top_bar=0,
            back_url=None,
            show_full_screen_btn=0,
            show_speed_btn=0,
            disable_drag=0
    ):
        """
        学课/考试页面接口

        :param _from: 平台类型，1：手机端; 2:PC端
        :param trainplan_id: 计划ID
        :param resources_id: 课程ID
        :param login_name: 当前登录的用户名称
        :param hide_top_bar: 是否隐藏顶部菜单栏
        :param back_url: 返回按钮的链接地址
        :param show_full_screen_btn: h5学课是否显示全屏按钮
        :param show_speed_btn: 是否显示倍速
        :param disable_drag: 是否禁止进度条拖拽
        :return: url
        """
        return self._gen_page(
            '/v1/open/lesson_open',
            _from=_from,
            trainplan_id=trainplan_id,
            resources_id=resources_id,
            login_name=login_name,
            hide_top_bar=hide_top_bar,
            back_url=back_url,
            show_full_screen_btn=show_full_screen_btn,
            show_speed_btn=show_speed_btn,
            disable_drag=disable_drag,
        )


    def paper_history(
            self,
            _from,
            trainplan_id,
            resources_id,
            login_name,
            hide_top_bar=False,
            back_url=None,
            show_full_screen_btn=True,
            show_speed_btn=False,
            disable_drag=False
    ):
        """
        考试历史页面接口

        :param _from: 平台类型，1：手机端; 2:PC端
        :param trainplan_id: 计划ID
        :param resources_id: 课程ID
        :param login_name: 当前登录的用户名称
        :param hide_top_bar: 是否隐藏顶部菜单栏
        :param back_url: 返回按钮的链接地址
        :param show_full_screen_btn: h5学课是否显示全屏按钮
        :param show_speed_btn: 是否显示倍速
        :param disable_drag: 是否禁止进度条拖拽
        :return: url
        """

        return self._gen_page(
            '/v1/open/paper_history',
            _from=_from,
            trainplan_id=trainplan_id,
            resources_id=resources_id,
            login_name=login_name,
            hide_top_bar=hide_top_bar,
            back_url=back_url,
            show_full_screen_btn=show_full_screen_btn,
            show_speed_btn=show_speed_btn,
            disable_drag=disable_drag,
        )

    def learn_rate_open(self, _from, trainplan_id, resources_id, login_name):
        """
        获取学习进度接口

        :param _from: 平台类型，1：手机端; 2:PC端
        :param trainplan_id: 计划ID
        :param resources_id: 课程ID
        :param login_name: 当前登录的用户名称
        """
        assert _from in (1, 2)
        return self._post('/v1/open/learn_rate_open', {
            'from': _from,
            'company_code': self.company_code,
            'trainplan_id': trainplan_id,
            'resources_id': resources_id,
            'login_name': login_name
        })

    def learn_rate_open_batch(self, _from, data=()):
        """
        批量获取学习进度接口

        :param _from: 平台类型，1：手机端; 2:PC端
        :param data: 请求数据 格式：```[
                                        ("计划id", "课程id", "当前登录的用户名称"),
                                        {
                                            "trainplan_id": "计划id",
                                            "resources_id": "课程id",
                                            "login_name": "当前登录的用户名称"
                                        }
                                   ]```
        """
        assert _from in (1, 2)
        _data = list()
        for d in data:
            sub_data = dict()
            if isinstance(d, (list, tuple)):
                assert len(d) == 3
                sub_data["trainplan_id"], sub_data["resources_id"], sub_data["login_name"] = d
            elif isinstance(d, dict):
                sub_data["trainplan_id"] = d["trainplan_id"]
                sub_data["resources_id"] = d["resources_id"]
                sub_data["login_name"] = d["login_name"]
            else:
                raise TypeError("data type error " + d)
            _data.append(sub_data)

        return self._post('/v1/open/learn_rate_open_batch', {
            'from': _from,
            'company_code': self.company_code,
            'data': json.dumps(_data),
        })

    def paper_rate_open_batch(self, _from, data=()):
        """
        批量获取用户历史考试接口

        :param _from: 平台类型，1：手机端; 2:PC端
        :param data: 请求数据 格式：[("计划id", "试卷ID"), {"trainplan_id": "计划id", "resources_id": "试卷ID"}]
        """
        assert _from in (1, 2)
        _data = list()
        for d in data:
            sub_data = dict()
            if isinstance(d, (list, tuple)):
                assert len(d) == 2
                sub_data["trainplan_id"], sub_data["resources_id"] = d
            elif isinstance(d, dict):
                sub_data["trainplan_id"] = d["trainplan_id"]
                sub_data["resources_id"] = d["resources_id"]
            else:
                raise TypeError("data type error " + d)
            _data.append(sub_data)

        return self._post('/v1/open/paper_rate_open_batch', {
            'from': _from,
            'company_code': self.company_code,
            'data': json.dumps(_data),
        })
