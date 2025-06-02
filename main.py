# 程序入口
import os
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from database import load_all, init_db
from qt_scheduler import init_scheduler
from gui import ReminderGUI
from reminder import ReminderManager
from tray import SystemTray

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 1) 初始化数据库（若已存在则跳过）
    init_db()

    # 2) 创建调度 & 加载已有任务
    mgr = ReminderManager()
    for rec in mgr.load_all():
        if rec['mode'] == 'interval':
            #传入job_id=rec['id']
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
    icon_path = os.path.join(os.path.dirname(__file__), 'icon', 'memento.ico')
    tray = SystemTray(icon_path=icon_path, parent_window=window)
    icon_path_2 = os.path.join(os.path.dirname(__file__), 'icon', 'memento_dark.ico')
    window.setWindowIcon(QIcon(icon_path_2))
    window.show()
    sys.exit(app.exec_())
