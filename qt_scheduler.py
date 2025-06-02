# qt_scheduler.py
from PyQt5.QtCore import QTimer, QDateTime
from notifier import show_notification
import time

class PollingScheduler:
    def __init__(self, interval_ms=1000):
        # task 格式：
        #   {'id': job_id, 'type':'interval','interval':60,'last':timestamp,'title':..., 'msg':...}
        #   {'id': job_id, 'type':'daily',   'hour':8, 'minute':0, 'last_date': 'YYYY-MM-DD', 'title':..., 'msg':...}
        self.tasks = {}
        self.timer = QTimer()
        self.timer.setInterval(interval_ms)
        self.timer.timeout.connect(self._tick)

    def start(self):
        self.timer.start()

    def add_interval(self, minutes, title, message, job_id=None):
        if job_id is None:
            job_id = f"interval_{int(time.time())}"
        self.tasks[job_id] = {
            'type':'interval',
            'interval': minutes*60,
            'last': time.time(),
            'title': title,
            'msg': message
        }
        return job_id

    def add_daily(self, hour, minute, title, message, job_id=None):
        if job_id is None:
            job_id = f"daily_{hour:02d}{minute:02d}_{int(time.time())}"
        today = QDateTime.currentDateTime().toString("yyyy-MM-dd")
        self.tasks[job_id] = {
            'type':'daily',
            'hour': hour,
            'minute': minute,
            'last_date': today,
            'triggered_today': False,
            'title': title,
            'msg': message
        }
        return job_id

    def remove(self, job_id):
        self.tasks.pop(job_id, None)

    t0 = time.perf_counter()#DEBUG

    def _tick(self):
        now = time.time()
        print(f"[Scheduler Tick] tasks={list(self.tasks.keys())}")  # 打印当前所有任务#DEBUG
        today_str = QDateTime.currentDateTime().toString("yyyy-MM-dd")
        for job_id, task in list(self.tasks.items()):
            print(f"  Checking {job_id}: {task}")
            if task['type']=='interval':
                if now - task['last'] >= task['interval']:
                    show_notification(task['title'], task['msg'])
                    task['last'] = now
            else:  # daily
                dt = QDateTime.currentDateTime()
                current_hour = dt.time().hour()
                current_minute = dt.time().minute()
                today_str = dt.toString("yyyy-MM-dd")

                if task['last_date'] != today_str:
                    # 新的一天，重置触发标志
                    task['last_date'] = today_str
                    task['triggered_today'] = False

                if (current_hour == task['hour'] and current_minute == task['minute']
                        and not task.get('triggered_today', False)):
                    show_notification(task['title'], task['msg'])
                    task['triggered_today'] = True

    print("Tick 耗时:", time.perf_counter() - t0)#DEBUG

scheduler = None

def init_scheduler(interval_ms=1000):
    global scheduler
    if scheduler is None:
        scheduler = PollingScheduler(interval_ms)
        scheduler.start()
    return scheduler
