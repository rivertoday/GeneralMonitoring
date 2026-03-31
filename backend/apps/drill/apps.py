"""
演练监督模块 - App配置
"""
from django.apps import AppConfig


class DrillConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.drill'
    verbose_name = '应急演练监督'

