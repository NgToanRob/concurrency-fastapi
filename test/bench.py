import requests
import concurrent.futures
import time

# URL của các endpoint
start_task_url = 'http://127.0.0.1:8000/start-task/'
task_status_url = 'http://127.0.0.1:8000/task-status/'

# Danh sách các task_id
task_ids = [1, 2, 3, 4, 5]

# Hàm thực hiện request POST với task_id được cung cấp
def start_task(task_id):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = {
        'task_id': f'unique_task_id_{task_id}'
    }
    response = requests.post(start_task_url, headers=headers, json=data)
    return response.json()['task_id']

# Hàm kiểm tra trạng thái của một tác vụ
def check_task_status(task_id):
    url = f'{task_status_url}{task_id}'
    response = requests.get(url)
    return response.json()

# Sử dụng ThreadPoolExecutor để thực hiện đồng thời các request
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    # Gửi các request và thu thập task_id
    task_ids_result = list(executor.map(start_task, task_ids))

# Kiểm tra trạng thái của các task_id
completed = [False] * len(task_ids_result)
while not all(completed):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Kiểm tra trạng thái các tác vụ
        statuses = list(executor.map(check_task_status, task_ids_result))
    
    # Cập nhật trạng thái hoàn thành
    for i, status in enumerate(statuses):
        if status['status'] == 'SUCCESS':
            completed[i] = True
        print(f'Task {task_ids_result[i]} status: {status}')
    
    # Đợi một khoảng thời gian trước khi kiểm tra lại
    time.sleep(1)

print("All tasks are completed.")
