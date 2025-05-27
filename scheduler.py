# scheduler.py 负责时间
import time
from apscheduler.events import EVENT_JOB_ERROR
from apscheduler.schedulers.qt import QtScheduler
from notifier import show_notification

# 全局任务错误监听器

def job_error_listener(event):
    """
    APScheduler 任务执行出错时的回调，用于打印错误信息
    """
    print(f"[调度器错误] 任务 {event.job_id} 执行失败：{event.exception}")

class ReminderScheduler:
    def __init__(self):
        # 使用 QtScheduler 将调度放到 Qt 事件循环中，避免多线程冲突
        self.scheduler = QtScheduler()
        self.scheduler.start()
        # 添加全局错误监听器
        self.scheduler.add_listener(job_error_listener, EVENT_JOB_ERROR)

#TODO:让这里的title变成可以手动修改内容的
    def add_interval_job(self, minutes: int, message: str) -> str:
        """
        添加间隔提醒任务（每隔 minutes 分钟执行一次）
        :param minutes: 间隔分钟数
        :param message: 提醒消息内容
        :return: 任务 ID
        """
        job_id = f"interval_{int(time.time())}"
        # 调度任务时传入默认标题和消息内容，匹配通知函数签名
        self.scheduler.add_job(
            func=lambda: show_notification("定时提醒", message),
            trigger="interval",
            minutes=minutes,
            id=job_id,
            replace_existing=False
        )
        return job_id

    def add_daily_job(self, hour: int, minute: int, message: str) -> str:
        """
        添加每天固定时间提醒任务（如每天 hour:minute 执行一次）
        :param hour: 小时（0-23）
        :param minute: 分钟（0-59）
        :param message: 提醒消息内容
        :return: 任务 ID
        """
        job_id = f"daily_{hour:02d}{minute:02d}_{int(time.time())}"
        self.scheduler.add_job(
            func=lambda: show_notification("定时提醒", message),
            trigger="cron",
            day="*",
            hour=hour,
            minute=minute,
            id=job_id,
            replace_existing=False
        )
        return job_id
