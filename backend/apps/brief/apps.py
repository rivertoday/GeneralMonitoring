"""
简报模块 - App配置
"""
from django.apps import AppConfig


class BriefConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.brief'
    verbose_name = '平急两用简报'

