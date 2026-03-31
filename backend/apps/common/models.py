"""
公共模型基类
"""
from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    """
    基础模型类，提供软删除和时间戳功能
    所有模型都应继承此类
    """
    created_at = models.DateTimeField('创建时间', auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    deleted_at = models.DateTimeField('删除时间', null=True, blank=True, db_index=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def delete(self, using=None, keep_parents=False):
        """软删除：设置deleted_at字段"""
        self.deleted_at = timezone.now()
        self.save(using=using)

    def hard_delete(self):
        """硬删除：真正从数据库中删除"""
        super().delete()

    @property
    def is_deleted(self):
        """判断是否已删除"""
        return self.deleted_at is not None

    def restore(self):
        """恢复已删除的记录"""
        self.deleted_at = None
        self.save()

