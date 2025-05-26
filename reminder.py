# 提醒任务类、提醒管理器
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import time
from plyer import notification  # 用于弹出Windows系统消息提醒

import notifier

scheduler = BackgroundScheduler()
scheduler.start()

##间隔提醒
def add_interval_reminder(interval_minutes, message):
    """
    添加一个间隔提醒任务（每隔 interval_minutes 分钟执行一次）
    """
    job_id = f'interval_{int(time.time())}'
    scheduler.add_job(
        notifier.show_notification,
        'interval',
        minutes=interval_minutes,
        args=[message],
        id=job_id,
        replace_existing=False
    )
    return job_id  # 返回任务 ID，以便后续修改或删除

# ✅ 指定日期和时间提醒一次（如 2025-06-01 08:00）
def add_datetime_reminder(datetime_obj: datetime, message: str):
    job_id = f'datetime_{int(time.time())}'
    scheduler.add_job(
        notifier.show_notification,
        'date',
        run_date=datetime_obj,
        args=[message],
        id=job_id,
        replace_existing=False
    )
    return job_id


# ✅ 每天固定时间提醒（如每天 08:00 提醒一次）
def add_daily_reminder(hour: int, minute: int, message: str):
    job_id = f'daily_{hour:02d}{minute:02d}_{int(time.time())}'
    scheduler.add_job(
        notifier.show_notification,
        'cron',
        day='*',
        hour=hour,
        minute=minute,
        args=[message],
        id=job_id,
        replace_existing=False
    )
    return job_id

def add_weekly_reminder(weekdays, hour, minute, message):
    # APScheduler 的星期参数是mon,tue,wed等字符串，需要转换
    day_map = {0: 'mon', 1: 'tue', 2: 'wed', 3: 'thu', 4: 'fri', 5: 'sat', 6: 'sun'}
    days_str = ','.join(day_map[d] for d in weekdays)
    job_id = f"weekly_{days_str}_{hour}_{minute}_{int(time.time())}"
    scheduler.add_job(
        notifier.show_notification,
        'cron',
        day_of_week=days_str,
        hour=hour,
        minute=minute,
        args=[message],
        id=job_id,
        replace_existing=False
    )
    return job_id

def add_monthly_reminder(days, hour, minute, message):
    # days 是日期列表，如 [1,15,28]
    days_str = ','.join(str(d) for d in days)
    job_id = f"monthly_{days_str}_{hour}_{minute}_{int(time.time())}"
    scheduler.add_job(
        notifier.show_notification,
        'cron',
        day=days_str,
        hour=hour,
        minute=minute,
        args=[message],
        id=job_id,
        replace_existing=False
    )
    return job_id