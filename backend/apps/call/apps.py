"""
叫应模块 - App配置
"""
from django.apps import AppConfig


class CallConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.call'
    verbose_name = '平急两用叫应'

