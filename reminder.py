# reminder.py 通知、接口包装

from qt_scheduler import init_scheduler
import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")#DEBUG

def add_interval_reminder(minutes, title, message):
    scheduler = init_scheduler()   # 如果尚未初始化，就在这里初始化
    return scheduler.add_interval(minutes, title, message)

def add_daily_reminder(hour, minute, title, message):
    scheduler = init_scheduler()
    return scheduler.add_daily(hour, minute, title, message)

def remove_reminder(job_id):
    scheduler = init_scheduler()
    logging.debug(f"Calling remove_reminder({job_id})")#DEBUG
    scheduler.remove(job_id)
    logging.debug(f"After remove, remaining tasks: {list(scheduler.tasks.keys())}")#DEBUG
