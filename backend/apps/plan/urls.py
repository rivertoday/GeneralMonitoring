"""
预案模块 - URL配置
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EmergencyPlanViewSet, PlanStructureViewSet, PlanFlowViewSet,
    PlanTaskViewSet, PlanExecutionViewSet, PlanTaskExecutionViewSet
)

router = DefaultRouter()
router.register(r'plans', EmergencyPlanViewSet, basename='emergency-plan')
# 保留独立路由以支持向后兼容
router.register(r'structures', PlanStructureViewSet, basename='plan-structure')
router.register(r'flows', PlanFlowViewSet, basename='plan-flow')
router.register(r'tasks', PlanTaskViewSet, basename='plan-task')
router.register(r'executions', PlanExecutionViewSet, basename='plan-execution')
router.register(r'task-executions', PlanTaskExecutionViewSet, basename='plan-task-execution')

urlpatterns = [
    path('', include(router.urls)),
    # 嵌套路由：支持 /plans/{plan_id}/structures/ 等嵌套路径
    path('plans/<int:plan_pk>/structures/', PlanStructureViewSet.as_view({'get': 'list', 'post': 'create'}), name='plan-structure-list'),
    path('plans/<int:plan_pk>/structures/tree/', PlanStructureViewSet.as_view({'get': 'tree'}), name='plan-structure-tree'),
    path('plans/<int:plan_pk>/structures/<int:pk>/', PlanStructureViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='plan-structure-detail'),
    path('plans/<int:plan_pk>/flows/', PlanFlowViewSet.as_view({'get': 'list', 'post': 'create'}), name='plan-flow-list'),
    path('plans/<int:plan_pk>/flows/tree/', PlanFlowViewSet.as_view({'get': 'tree'}), name='plan-flow-tree'),
    path('plans/<int:plan_pk>/flows/<int:pk>/', PlanFlowViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='plan-flow-detail'),
    path('plans/<int:plan_pk>/tasks/', PlanTaskViewSet.as_view({'get': 'list', 'post': 'create'}), name='plan-task-list'),
    path('plans/<int:plan_pk>/tasks/<int:pk>/', PlanTaskViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='plan-task-detail'),
]

