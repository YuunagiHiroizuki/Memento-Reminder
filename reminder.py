# reminder.py 通知、接口包装

from scheduler import ReminderScheduler

_sched = ReminderScheduler()

def add_interval_reminder(minutes, message):
    return _sched.add_interval_job(minutes, message)

def add_daily_reminder(hour, minute, message):
    return _sched.add_daily_job(hour, minute, message)
