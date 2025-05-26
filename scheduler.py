# APScheduler 调度器封装
import time

from apscheduler.schedulers.background import BackgroundScheduler
from notifier import show_notification

class ReminderScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

    def add_interval_job(self, minutes: int, message: str):
        job_id = f'interval_{int(time.time())}'  # 以当前时间生成唯一ID
        self.scheduler.add_job(
            func=lambda: show_notification("提醒", message),
            trigger="interval",
            minutes=minutes,
            id=job_id,  # 用生成的 job_id 来注册
            replace_existing=False
        )
        return job_id
