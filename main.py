# 程序入口
import sys
from PyQt5.QtWidgets import QApplication
from gui import ReminderGUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ReminderGUI()
    window.show()
    sys.exit(app.exec_())
