from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler
from rest_framework.views import Response


class BarException(APIException):
    code = 1000  # 0表示成功，非零表示失败
    message = '未知异常，请联系管理员'

    @classmethod
    def get_message(cls):
        return {'code': cls.code, 'message': cls.message}


class NotFound(BarException):
    code = 10000
    message = '找不到数据'


class InvalidToken(BarException):
    code = 5
    message = "登录无效，请重新登录"


class InvalidUsernameOrPassword(BarException):
    code = 1
    message = "Wrong user name or password,Please log in again!"
# 'DRF异常名'：异常类
exc_map = {
    'DoesNotExist': NotFound,
    'InvalidToken': InvalidToken,
    'AuthenticationFailed': InvalidUsernameOrPassword
}


def global_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    print("=" * 30)
    print(exc, type(exc), response)
    # Now add the HTTP status code to the response.
    # if response is not None:
    #     message = exc_map.get(exc.__class__.__name__, BarException).get_message()
    #     return Response({'message': '平安无事'})

    if isinstance(exc, BarException):
        message = exc.get_message()
    else:
        message = exc_map.get(exc.__class__.__name__, BarException).get_message()

    return Response(message, status=200)  # 200成功回调，400失败回调