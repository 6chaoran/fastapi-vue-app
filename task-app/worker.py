import redis
r = redis.StrictRedis(host = "localhost", decode_responses=True)
ping = r.ping()
print(f"Redis Ping Result: {ping}")

import time

if __name__ == '__main__':
    idle = False
    while True:
        task_id = r.rpop('tasks')
        if task_id:
            idle = False
            print(f'processing task[{task_id}]')
            for i in range(5):
                r.hset(f'task:{task_id}', 'status', f'{i/5:.0%}')
                time.sleep(1)
            r.hset(f'task:{task_id}', 'status', 'done')
        else:
            if not idle:
                print('no more tasks, waiting ...')
                idle = True
            time.sleep(5)
