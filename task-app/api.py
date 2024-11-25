# FastAPI
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

import subprocess
from multiprocessing import Process
import sys

# Run workers
def run_worker():
    python_path = sys.executable 
    subprocess.run([python_path, "worker.py"])

from datetime import datetime
import redis
r = redis.StrictRedis(host = "localhost", decode_responses=True)
ping = r.ping()
print(f"Redis Ping Result: {ping}")
r.flushall()
app = FastAPI()

class Task(BaseModel):
    task_id: str

# vue app URL
# load ui from app.html

@app.get("/app")
def read_index():
    return FileResponse("./app.html")

@app.post("/submit_task")
def submit_task(task: Task):
    task_id = task.task_id
    r.hset(f'task:{task_id}', 'status', 'queued')
    r.hset(f'task:{task_id}', 'created_at', datetime.now().isoformat()[:19].replace('T', ' '))
    r.lpush('tasks', task_id)
    print(f'task[{task_id}] pushed to queue')
    return {'status': 'ok'}

@app.get("/task_status")
def get_task_status():
    tasks = []
    for task in r.scan_iter('task:*'):
        status = r.hget(task, 'status')
        created_at = r.hget(task, 'created_at')
        tasks.append({'task_id': task, 'status': status, 'created_at': created_at})
    return{'tasks': tasks}

if __name__ == "__main__":
    process = Process(target = run_worker)
    process.start()
    import uvicorn
    uvicorn.run(app, host ="localhost", port = 8000)
