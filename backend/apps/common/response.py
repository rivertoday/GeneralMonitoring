"""
统一响应格式
"""
from rest_framework.response import Response
from rest_framework import status


class APIResponse(Response):
    """
    统一API响应格式
    {
        "code": 200,
        "message": "success",
        "data": {...}
    }
    """
    
    def __init__(self, data=None, message='success', code=200, status_code=status.HTTP_200_OK, **kwargs):
        response_data = {
            'code': code,
            'message': message,
            'data': data
        }
        super().__init__(data=response_data, status=status_code, **kwargs)


class SuccessResponse(APIResponse):
    """成功响应"""
    def __init__(self, data=None, message='操作成功', **kwargs):
        super().__init__(data=data, message=message, code=200, **kwargs)


class ErrorResponse(APIResponse):
    """错误响应"""
    def __init__(self, message='操作失败', code=400, status_code=status.HTTP_400_BAD_REQUEST, **kwargs):
        super().__init__(data=None, message=message, code=code, status_code=status_code, **kwargs)


