# 程序入口
import sys
from PyQt5.QtWidgets import QApplication

from database import load_all, init_db
from qt_scheduler import init_scheduler
from gui import ReminderGUI
from reminder import ReminderManager

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 1) 初始化数据库（若已存在则跳过）
    init_db()

    # 2) 创建调度 & 加载已有任务
    mgr = ReminderManager()
    for rec in mgr.load_all():
        if rec['mode'] == 'interval':
            # 一定要传 job_id=rec['id']，不要再让它生成新 ID！
            mgr.sched.add_interval(
                rec['interval'],
                rec['title'],
                rec['message'],
                job_id=rec['id']
            )
        else:
            h, m = map(int, rec['time'].split(':'))
            mgr.sched.add_daily(
                h, m,
                rec['title'],
                rec['message'],
                job_id=rec['id']
            )

    init_scheduler(interval_ms=1000)    #初始化并启动定时器
    mgr = ReminderManager()
    window = ReminderGUI(mgr)
    window.show()
    sys.exit(app.exec_())
