from celery import Celery
from redlock import Redlock
import time
import redis


app = Celery(
    'tasks',
    broker='pyamqp://user:password@rabbitmq//',
    backend='redis://redis:6379/0',
)

# Khởi tạo kết nối tới Redis
redis_client = redis.StrictRedis(host='redis', port=6379, db=0)

# Khởi tại resource_in_use
if not redis_client.exists('resource_in_use'):
    redis_client.set('resource_in_use', '0')

# Khởi tạo Redlock
dlm = Redlock([{"host": "redis", "port": 6379, "db": 0},
               {"host": "redis", "port": 6379, "db": 1},
               {"host": "redis", "port": 6379, "db": 2}])

@app.task
def long_task(task_id: str):
    while True:
        # Cố gắng lấy khóa với thời gian timeout là 10 giây
        lock = dlm.lock("resource_in_use", 10000)
        if lock:
            try:
                print('Lock acquired!')
                # Phát tín hiệu dừng tất cả các worker khác
                redis_client.set('resource_in_use', '1')
                return 'Ready to unlock'
            finally:
                # Đánh dấu tài nguyên là không sử dụng
                dlm.unlock(lock)
                # Giả lập thời gian xử lý công việc
                time.sleep(5)
                # Phát tín hiệu cho tất cả các worker khác chạy tiếp
                redis_client.set('resource_in_use', '0')
        else:
            print("Failed to acquire lock, retrying immediately...")
