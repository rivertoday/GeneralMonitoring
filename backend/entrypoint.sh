#!/bin/bash
set -e

echo "=========================================="
echo "风险监测预警系统 - 容器启动脚本"
echo "=========================================="

# 等待数据库就绪（可选，如果需要）
# 这里假设数据库已经在运行，如果需要等待可以添加检查逻辑

# 创建必要的目录
echo "创建必要的目录..."
mkdir -p /app/backend/logs
mkdir -p /app/backend/media
mkdir -p /app/backend/staticfiles

# 设置权限
chmod -R 755 /app/backend/logs
chmod -R 755 /app/backend/media
chmod -R 755 /app/backend/staticfiles

# 执行数据库迁移
# 注意：此命令是安全的，如果数据库结构没有变化，会快速完成且不影响已有数据
# 如果后续有模型更新，迁移会自动应用新的数据库结构
echo "执行数据库迁移..."
python manage.py migrate --noinput

# 收集静态文件
echo "收集静态文件..."
python manage.py collectstatic --noinput --clear

# 创建超级用户（可选，仅在首次部署时使用）
# 如果需要，可以通过环境变量控制
# if [ "$CREATE_SUPERUSER" = "true" ]; then
#     echo "创建超级用户..."
#     python manage.py createsuperuser --noinput || true
# fi

# 启动 Gunicorn
echo "启动 Gunicorn 服务器..."
exec gunicorn config.wsgi:application \
    --config gunicorn_config.py \
    --bind 0.0.0.0:8000 \
    --access-logfile - \
    --error-logfile - \
    --log-level info

