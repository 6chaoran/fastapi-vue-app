import redis
import time

if __name__ == '__main__':
    r = redis.StrictRedis(host = "localhost", decode_responses=True)
    ping = r.ping()
    print(f"Redis Ping Result from worker: {ping}")
    idle = False
    while True:
        task_id = r.rpop('tasks')
        if task_id:
            idle = False
            msgs = []
            print(f'processing task[{task_id}]')
            msgs += [f'processing task[{task_id}]']
            for i in range(5):
                r.hset(f'task:{task_id}', 'status', f'{i/5:.0%}')
                msgs += [f"progress: {i/5:.0%}"]
                r.hset(f'task:{task_id}', 'msg', '<br>'.join(msgs))
                time.sleep(1)
            r.hset(f'task:{task_id}', 'status', 'done')
            msgs += ['done!']
            r.hset(f'task:{task_id}', 'msg', '<br>'.join(msgs))
        else:
            if not idle:
                print('no more tasks, waiting ...')
                idle = True
            time.sleep(1)
