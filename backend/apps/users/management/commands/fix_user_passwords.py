"""
修复用户密码的管理命令
在加载fixtures后，使用此命令为所有用户设置正确的密码
"""
from django.core.management.base import BaseCommand
from apps.users.models import User


class Command(BaseCommand):
    help = '为所有用户设置默认密码（123456）'

    def add_arguments(self, parser):
        parser.add_argument(
            '--password',
            type=str,
            default='123456',
            help='要设置的密码（默认：123456）',
        )

    def handle(self, *args, **options):
        password = options['password']
        
        users = User.objects.filter(deleted_at__isnull=True)
        count = 0
        
        for user in users:
            user.set_password(password)
            user.save()
            count += 1
            self.stdout.write(
                self.style.SUCCESS(f'✓ 用户 {user.username} 密码已更新')
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'\n成功更新 {count} 个用户的密码')
        )

