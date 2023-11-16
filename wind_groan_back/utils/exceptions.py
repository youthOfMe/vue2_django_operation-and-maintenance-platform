from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.views import exception_handler

class MagBaseException(exceptions.APIException):
    code = 10000 # code为0表示正常，非0都是异常
    message = "未知错误，请联系管理员"

    @classmethod
    def get_message(cls):
        return {'code': cls.code, 'message': cls.message}

class InvalidUsernameOrPassword(MagBaseException):
    code = 1
    message = '用户名或密码错误，请重新登录'


# Django Drf异常类 我要做映射和替换
exc_map = {
    'AuthenticationFailed': InvalidUsernameOrPassword
}


def global_exception_handler(exc, context):
    print(exc, type(exc), '!!!!!!!!!!!!!!!!!!!!!!!!!!')
    # 调用DRF提供异常处理器
    # response None 500
    # response Response对象 APIException
    response = exception_handler(exc, context)
    print('~' * 30)
    print(type(exc), exc.__dict__)
    print('~' * 30)

    if response is not None:
        # 提供最终用户更加友好的提示、阻止某些技术导致的异常信息返回
        # 从一种异常类型 映射 到另一种异常
        if isinstance(exc, MagBaseException):
            errmsg = exc.get_message()
        else:
            errmsg = exc_map.get(exc.__class__.__name__, MagBaseException).get_message()
        return Response(errmsg, status=200) # 恒为200
    return response

