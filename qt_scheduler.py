from PyQt5.QtCore import QTimer
import subprocess
import time

class QtReminderScheduler:
    def __init__(self):
        self.jobs = {}  # job_id: QTimer

    def add_interval_job(self, minutes: int, title: str, message: str) -> str:
        job_id = f"interval_{int(time.time())}"
        timer = QTimer()
        timer.setInterval(minutes * 60 * 1000)  # 转毫秒
        timer.timeout.connect(lambda: self._trigger_notification(title, message))
        timer.start()
        self.jobs[job_id] = timer
        return job_id

    def add_daily_job(self, hour: int, minute: int, title: str, message: str) -> str:
        from datetime import datetime, timedelta

        job_id = f"daily_{hour:02d}{minute:02d}_{int(time.time())}"

        def schedule_next():
            now = datetime.now()
            target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            if target <= now:
                target += timedelta(days=1)
            delta_ms = int((target - now).total_seconds() * 1000)

            timer = QTimer()
            timer.setSingleShot(True)
            timer.setInterval(delta_ms)
            timer.timeout.connect(lambda: trigger_and_reschedule())
            timer.start()
            self.jobs[job_id] = timer

        def trigger_and_reschedule():
            self._trigger_notification(title, message)
            schedule_next()

        schedule_next()
        return job_id

    def _trigger_notification(self, title, message):
        subprocess.Popen(["python", "notifier.py", title, message])
