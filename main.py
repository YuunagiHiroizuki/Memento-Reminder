# 程序入口
import sys
from PyQt5.QtWidgets import QApplication
from qt_scheduler import init_scheduler
from gui import ReminderGUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    init_scheduler(interval_ms=1000)    #初始化并启动定时器
    window = ReminderGUI()
    window.show()
    sys.exit(app.exec_())

