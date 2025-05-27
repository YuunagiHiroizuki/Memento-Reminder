# gui.py
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QTabWidget, QListWidget
)
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt
from reminder import add_interval_reminder, add_daily_reminder

class ReminderGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("定时提醒工具")
        self.setFixedSize(400, 360)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # 顶部选项卡
        self.tabs = QTabWidget()

        # Tab1: 间隔提醒
        self.interval_tab = QWidget()
        interval_layout = QVBoxLayout()
        interval_layout.setSpacing(8)
        interval_layout.addWidget(QLabel("每隔几分钟提醒："))
        self.input_minutes = QLineEdit()
        self.input_minutes.setValidator(QIntValidator(1, 1440, self))
        self.input_minutes.setPlaceholderText("例如 30")
        interval_layout.addWidget(self.input_minutes)
        interval_layout.addWidget(QLabel("提醒内容："))
        self.input_message = QLineEdit()
        self.input_message.setPlaceholderText("例如：起来活动一下~")
        interval_layout.addWidget(self.input_message)
        self.add_interval_btn = QPushButton("添加间隔提醒")
        self.add_interval_btn.clicked.connect(self.on_add_interval_clicked)
        interval_layout.addWidget(self.add_interval_btn)
        # 单独展示间隔提醒任务
        interval_layout.addWidget(QLabel("间隔提醒列表："))
        self.interval_list = QListWidget()
        interval_layout.addWidget(self.interval_list)
        self.interval_tab.setLayout(interval_layout)

        # Tab2: 每日提醒
        self.daily_tab = QWidget()
        daily_layout = QVBoxLayout()
        daily_layout.setSpacing(8)
        time_layout = QHBoxLayout()
        time_layout.setSpacing(5)
        time_layout.addStretch(1)
        self.input_hour = QLineEdit()
        self.input_hour.setValidator(QIntValidator(0, 23, self))
        self.input_hour.setFixedWidth(50)
        self.input_hour.setPlaceholderText("08")
        time_layout.addWidget(self.input_hour)
        colon = QLabel(":")
        colon.setFixedWidth(10)
        colon.setAlignment(Qt.AlignCenter)
        time_layout.addWidget(colon)
        self.input_minute = QLineEdit()
        self.input_minute.setValidator(QIntValidator(0, 59, self))
        self.input_minute.setFixedWidth(50)
        self.input_minute.setPlaceholderText("00")
        time_layout.addWidget(self.input_minute)
        time_layout.addStretch(1)
        daily_layout.addLayout(time_layout)
        daily_layout.addWidget(QLabel("提醒内容："))
        self.daily_message = QLineEdit()
        self.daily_message.setPlaceholderText("例如：早餐时间~")
        daily_layout.addWidget(self.daily_message)
        self.add_daily_btn = QPushButton("添加每日提醒")
        self.add_daily_btn.clicked.connect(self.on_add_daily_clicked)
        daily_layout.addWidget(self.add_daily_btn)
        # 单独展示每日提醒任务
        daily_layout.addWidget(QLabel("每日提醒列表："))
        self.daily_list = QListWidget()
        daily_layout.addWidget(self.daily_list)
        self.daily_tab.setLayout(daily_layout)

        # 添加 tabs
        self.tabs.addTab(self.interval_tab, "间隔提醒")
        self.tabs.addTab(self.daily_tab, "每日提醒")
        main_layout.addWidget(self.tabs)

        self.setLayout(main_layout)

    def on_add_interval_clicked(self):
        interval = self.input_minutes.text().strip()
        message = self.input_message.text().strip()
        if not interval or not message:
            QMessageBox.warning(self, "错误", "请填写有效的提醒内容和时间间隔")
            return
        minutes = int(interval)
        job_id = add_interval_reminder(minutes, message)
        self.interval_list.addItem(f"[{job_id}] 间隔 {minutes} 分钟：{message}")
        QMessageBox.information(self, "成功", f"已添加每 {minutes} 分钟提醒一次：{message}")

    def on_add_daily_clicked(self):
        hour_str = self.input_hour.text().strip()
        minute_str = self.input_minute.text().strip()
        message = self.daily_message.text().strip()
        if not hour_str or not minute_str or not message:
            QMessageBox.warning(self, "错误", "请填写有效的时间和提醒内容")
            return
        hour = int(hour_str)
        minute = int(minute_str)
        job_id = add_daily_reminder(hour, minute, message)
        self.daily_list.addItem(f"[{job_id}] 每天 {hour:02d}:{minute:02d}：{message}")
        QMessageBox.information(self, "成功", f"已添加每天 {hour:02d}:{minute:02d} 提醒：{message}")

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = ReminderGUI()
    window.show()
    sys.exit(app.exec_())
