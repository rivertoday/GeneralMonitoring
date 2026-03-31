"""
演练监督模块 - URL配置
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DrillEventViewSet, DrillEvaluationViewSet,
    DrillSummaryViewSet, DrillAnalysisViewSet
)

router = DefaultRouter()
router.register(r'events', DrillEventViewSet, basename='drill-event')
router.register(r'evaluations', DrillEvaluationViewSet, basename='drill-evaluation')
router.register(r'summaries', DrillSummaryViewSet, basename='drill-summary')
router.register(r'analyses', DrillAnalysisViewSet, basename='drill-analysis')

urlpatterns = [
    path('', include(router.urls)),
]

