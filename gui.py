# PyQt5 GUI 控制
# gui.py
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox
)

from reminder import add_interval_reminder
from scheduler import ReminderScheduler

class ReminderGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("定时提醒工具")
        self.setFixedSize(300, 180)

        self.scheduler = ReminderScheduler()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.label1 = QLabel("每隔几分钟提醒：")
        self.input_minutes = QLineEdit()
        self.input_minutes.setPlaceholderText("例如 30")

        self.label2 = QLabel("提醒内容：")
        self.input_message = QLineEdit()
        self.input_message.setPlaceholderText("例如：起来活动一下~")

        self.button = QPushButton("添加提醒")
        self.button.clicked.connect(self.on_add_interval_clicked)

        layout.addWidget(self.label1)
        layout.addWidget(self.input_minutes)
        layout.addWidget(self.label2)
        layout.addWidget(self.input_message)
        layout.addWidget(self.button)

        self.setLayout(layout)

#获取用户输入，调用 add_interval_reminder
    def on_add_interval_clicked(self):
        try:
            interval = int(self.input_minutes.text())
            message = self.input_message.text()

            if interval <= 0 or not message:
                QMessageBox.warning(self, "错误", "请填写有效的提醒内容和时间间隔")
                return

            # 只调用scheduler的接口添加任务
            job_id = self.scheduler.add_interval_job(interval, message)
            print(f"添加了间隔提醒任务，任务ID: {job_id}")

            QMessageBox.information(self, "成功", f"已添加每 {interval} 分钟提醒一次：{message}")

        except ValueError:
            QMessageBox.warning(self, "错误", "请输入有效的数字作为时间间隔")
        except Exception as e:
            print(f"[错误] 添加提醒失败：{e}")
            QMessageBox.warning(self, "错误", "添加提醒时发生错误，请检查输入。")