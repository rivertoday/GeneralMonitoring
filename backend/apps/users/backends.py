"""
自定义认证后端 - JWT Token认证
"""
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomJWTAuthentication(JWTAuthentication):
    """
    自定义JWT认证后端
    用于从JWT Token中获取用户对象
    """
    
    def get_user(self, validated_token):
        """
        根据token中的用户ID获取用户对象
        """
        try:
            user_id = validated_token.get('user_id')
            user = User.objects.get(id=user_id, deleted_at__isnull=True, status=1)
            return user
        except User.DoesNotExist:
            raise InvalidToken('用户不存在或已被禁用')
        except Exception as e:
            raise InvalidToken(f'认证失败: {str(e)}')

