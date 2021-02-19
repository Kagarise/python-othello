import json


class Result(object):
    @staticmethod
    def success(data=None):
        return json.dumps({
            'code': 200,
            'msg': "success",
            'data': data
        }, ensure_ascii=False)

    @staticmethod
    def error(code, msg):
        return json.dumps({
            'code': code,
            'msg': msg
        }, ensure_ascii=False)
