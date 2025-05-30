# reminder.py 通知、接口包装

from qt_scheduler import init_scheduler
from database import (
    add_interval, add_daily,
    delete_reminder, update_interval, update_daily, load_all
)

class ReminderManager:
    def __init__(self):
        self.sched = init_scheduler()

    def schedule_interval(self, rid, minutes, title, message):
        job_id = self.sched.add_interval(minutes, title, message)
        return self.sched.add_interval(minutes, title, message, job_id=rid)

    def schedule_daily(self, rid, hour, minute, title, message):
        job_id = self.sched.add_daily(hour, minute, title, message)
        return self.sched.add_daily(hour, minute, title, message, job_id=rid)

    def add_interval(self, title, message, minutes):
        rid = add_interval(title, message, minutes)
        job_id = self.schedule_interval(rid, minutes, title, message)
        return rid

    def add_daily(self, title, message, hhmm):
        rid = add_daily(title, message, hhmm)
        h, m = map(int, hhmm.split(':'))
        job_id = self.schedule_daily(rid, h, m, title, message)
        return rid

    def remove(self, rid):
        delete_reminder(rid)
        self.sched.remove(rid)

    def modify_interval(self, rid, title, message, minutes):
        update_interval(rid, title, message, minutes)
        self.sched.remove(rid)
        self.sched.add_interval(minutes, title, message, job_id=rid)

    def modify_daily(self, rid, title, message, hhmm):
        update_daily(rid, title, message, hhmm)
        self.sched.remove(rid)
        h, m = map(int, hhmm.split(':'))
        self.sched.add_daily(h, m, title, message, job_id=rid)

    def load_all(self):
        """
        从数据库加载所有启用提醒，恢复调度并返回记录列表给 GUI:
        [
          {'id':..., 'mode':'interval', 'title':..., 'message':..., 'interval':...},
          {'id':..., 'mode':'daily',    'title':..., 'message':..., 'time':'HH:MM'},
          …
        ]
        """
        records = load_all()
        for r in records:
            rid, mode = r['id'], r['mode']
            title, message = r['title'], r['message']
            if mode == 'interval':
                minutes = r['interval']
                # 直接用 rid 作为 job_id 恢复
                self.sched.add_interval(minutes, title, message, job_id=rid)
            else:
                hh, mm = map(int, r['time'].split(':'))
                self.sched.add_daily(hh, mm, title, message, job_id=rid)
        return records

