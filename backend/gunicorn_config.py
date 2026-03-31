"""
Gunicorn 配置文件
用于生产环境部署
"""
import os
import multiprocessing

# 服务器套接字
bind = os.getenv('GUNICORN_BIND', '127.0.0.1:8000')

# 工作进程数
# 公式: (2 × CPU核心数) + 1
# 设置合理的默认值和上限（最多16个worker，避免资源耗尽）
cpu_count = multiprocessing.cpu_count()
default_workers = min(cpu_count * 2 + 1, 16)  # 最多16个worker
workers = int(os.getenv('GUNICORN_WORKERS', default_workers))
# 确保 workers 在合理范围内（1-32）
workers = max(1, min(workers, 32))

# 工作进程类型
worker_class = 'sync'
worker_connections = 1000

# 每个工作进程的线程数（如果使用线程）
threads = 1

# 超时设置（秒）
timeout = int(os.getenv('GUNICORN_TIMEOUT', 120))
keepalive = 5

# 日志配置
# 使用环境变量或默认路径（优先使用环境变量，否则使用项目目录下的 backend/logs）
log_dir = os.getenv('GUNICORN_LOG_DIR')
if not log_dir:
    # 如果未设置环境变量，使用项目目录下的 backend/logs
    # gunicorn_config.py 位于 /opt/risk-monitoring/backend/
    # 日志目录应为 /opt/risk-monitoring/backend/backend/logs
    import pathlib
    log_dir = str(pathlib.Path(__file__).parent / 'backend' / 'logs')
    os.makedirs(log_dir, exist_ok=True)
elif not os.path.exists(log_dir):
    # 如果环境变量指定的目录不存在，创建它
    os.makedirs(log_dir, exist_ok=True)

accesslog = os.path.join(log_dir, 'gunicorn_access.log')
errorlog = os.path.join(log_dir, 'gunicorn_error.log')
loglevel = os.getenv('LOG_LEVEL', 'info').lower()

# 进程名称
proc_name = 'risk_monitoring_backend'

# 守护进程模式（在 Docker 中不需要，由容器管理）
daemon = False

# 用户和组（在 Docker 中不需要，由容器管理）
# user = 'www-data'
# group = 'www-data'

# 临时目录
tmp_upload_dir = None

# 预加载应用（提高性能，但会增加内存使用）
preload_app = False

# 最大请求数（防止内存泄漏）
max_requests = 1000
max_requests_jitter = 50

# 优雅重启超时
graceful_timeout = 30

# 访问日志格式
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# 工作进程临时目录
worker_tmp_dir = '/dev/shm'

