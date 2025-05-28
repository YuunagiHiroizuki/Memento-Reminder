# reminder.py 通知、接口包装

from qt_scheduler import QtReminderScheduler

_sched = QtReminderScheduler()

def add_interval_reminder(minutes, title, message):
    return _sched.add_interval_job(minutes, title, message)

def add_daily_reminder(hour, minute, title, message):
    return _sched.add_daily_job(hour, minute, title, message)
