"""
清除区域态势数据的Django管理命令
使用方法：python manage.py clear_region_status
"""
from django.core.management.base import BaseCommand
from apps.safety.models import RegionStatus


class Command(BaseCommand):
    help = '清除所有区域态势数据'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='确认删除，不显示确认提示',
        )

    def handle(self, *args, **options):
        count = RegionStatus.objects.count()
        
        if count == 0:
            self.stdout.write(self.style.WARNING('区域态势表中没有数据'))
            return

        if not options['confirm']:
            self.stdout.write(self.style.WARNING(
                f'警告：将删除区域态势表中的 {count} 条记录'
            ))
            confirm = input('确认删除？(yes/no): ')
            if confirm.lower() != 'yes':
                self.stdout.write(self.style.ERROR('操作已取消'))
                return

        deleted_count, _ = RegionStatus.objects.all().delete()
        self.stdout.write(
            self.style.SUCCESS(f'成功删除 {deleted_count} 条区域态势记录')
        )

