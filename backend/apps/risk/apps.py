"""
风险监测预警模块 - App配置
"""
from django.apps import AppConfig


class RiskConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.risk'
    verbose_name = '风险监测预警'

