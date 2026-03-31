"""
预案模块 - App配置
"""
from django.apps import AppConfig


class PlanConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.plan'
    verbose_name = '应急预案数智化'

