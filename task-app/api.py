# FastAPI
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

import subprocess
import sys
from multiprocessing import Process

from datetime import datetime
import redis

# Run workers
def run_worker():
    python_path = sys.executable 
    subprocess.run([python_path, "worker.py"])  

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
    ids = task.task_id.split(',')
    for id in ids:
        task_id = id
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
        message = r.hget(task, 'msg')
        tasks.append({'task_id': task, 'status': status, 'created_at': created_at, 'message': message})
    return{'tasks': tasks}

if __name__ == "__main__":
    
    r = redis.StrictRedis(host = "localhost", decode_responses=True)
    ping = r.ping()
    print(f"Redis Ping Result from server: {ping}")
    r.flushall()
  
    processes = []
    for i in range(2):
        process = Process(target = run_worker)
        processes.append(process)
    for p in processes:
        p.start()

    import webbrowser
    webbrowser.open('http://localhost:8000/app', new = 2)
    import uvicorn
    uvicorn.run(app, host ="localhost", port = 8000)
