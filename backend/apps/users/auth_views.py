"""
用户认证视图 - JWT登录、刷新token等
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from apps.common.response import SuccessResponse, ErrorResponse
from .models import User
from .serializers import UserLoginSerializer, UserDetailSerializer


@swagger_auto_schema(
    method='post',
    tags=['认证'],
    operation_summary='用户登录',
    operation_description='用户登录获取JWT Token',
    request_body=UserLoginSerializer,
    responses={
        200: openapi.Response('登录成功', UserDetailSerializer),
        401: '用户名或密码错误',
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    用户登录
    POST /api/v1/auth/login/
    {
        "username": "admin",
        "password": "password123"
    }
    """
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    password = serializer.validated_data['password']

    try:
        # 查找用户（排除已删除的用户）
        user = User.objects.get(username=username, deleted_at__isnull=True)
    except User.DoesNotExist:
        return ErrorResponse(message='用户名或密码错误', code=401, status_code=status.HTTP_401_UNAUTHORIZED)

    # 验证密码
    if not user.check_password(password):
        return ErrorResponse(message='用户名或密码错误', code=401, status_code=status.HTTP_401_UNAUTHORIZED)

    # 检查用户状态
    if user.status != 1:
        return ErrorResponse(message='用户已被禁用', code=403, status_code=status.HTTP_403_FORBIDDEN)

    # 更新最后登录时间和IP
    ip_address = request.META.get('REMOTE_ADDR', None)
    user.update_last_login(ip_address)

    # 生成JWT Token
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    # 获取用户信息
    user_serializer = UserDetailSerializer(user)

    return SuccessResponse(
        data={
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user_serializer.data
        },
        message='登录成功'
    )


@swagger_auto_schema(
    method='post',
    tags=['认证'],
    operation_summary='刷新Token',
    operation_description='使用refresh token获取新的access token',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='refresh token')
        },
        required=['refresh']
    ),
    responses={
        200: openapi.Response('刷新成功'),
        401: 'Token无效',
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    """
    刷新Token
    POST /api/v1/auth/refresh/
    {
        "refresh": "refresh_token_string"
    }
    """
    refresh_token = request.data.get('refresh', None)

    if not refresh_token:
        return ErrorResponse(message='refresh token不能为空', code=400)

    try:
        refresh = RefreshToken(refresh_token)
        access_token = str(refresh.access_token)
        return SuccessResponse(
            data={
                'access_token': access_token
            },
            message='刷新成功'
        )
    except TokenError as e:
        return ErrorResponse(message=f'Token无效: {str(e)}', code=401, status_code=status.HTTP_401_UNAUTHORIZED)


@swagger_auto_schema(
    method='post',
    tags=['认证'],
    operation_summary='用户登出',
    operation_description='用户登出，将token加入黑名单',
    security=[{'Bearer': []}],
    responses={
        200: openapi.Response('登出成功'),
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    用户登出
    POST /api/v1/auth/logout/
    需要Authorization: Bearer <token>
    """
    try:
        refresh_token = request.data.get('refresh', None)
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()  # 将token加入黑名单（需要配置simplejwt的BLACKLIST_AFTER_ROTATION）
    except Exception:
        pass  # 忽略错误，即使token无效也返回成功

    return SuccessResponse(message='登出成功')


@swagger_auto_schema(
    method='get',
    tags=['认证'],
    operation_summary='获取当前用户信息',
    operation_description='获取当前登录用户的详细信息',
    security=[{'Bearer': []}],
    responses={
        200: openapi.Response('获取成功', UserDetailSerializer),
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    """
    获取当前用户信息
    GET /api/v1/auth/user-info/
    需要Authorization: Bearer <token>
    """
    serializer = UserDetailSerializer(request.user)
    return SuccessResponse(data=serializer.data)

