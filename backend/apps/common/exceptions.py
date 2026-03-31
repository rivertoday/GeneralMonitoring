"""
自定义异常处理
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    自定义异常处理器
    """
    # 调用DRF默认异常处理器
    response = exception_handler(exc, context)
    
    if response is not None:
        # 自定义响应格式
        custom_response_data = {
            'code': response.status_code,
            'message': '请求处理失败',
            'data': None,
            'errors': response.data if isinstance(response.data, dict) else {'detail': str(response.data)}
        }
        
        # 记录错误日志
        logger.error(f"API异常: {exc}, 上下文: {context}, 响应: {response.data}")
        
        return Response(custom_response_data, status=response.status_code)
    
    # 处理未捕获的异常
    logger.exception(f"未捕获的异常: {exc}, 上下文: {context}")
    
    return Response({
        'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
        'message': '服务器内部错误',
        'data': None,
        'errors': {'detail': '服务器内部错误，请稍后重试'}
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


