from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QTabWidget, QListWidget, QListWidgetItem
)
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt
from reminder import (
    add_interval_reminder,
    add_daily_reminder,
    remove_reminder
)

class ReminderGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("定时提醒工具")
        self.setFixedSize(400, 450)
        self.editing_interval_id = None
        self.editing_daily_id = None
        self.interval_tasks = {}
        self.daily_tasks = {}
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        self.tabs = QTabWidget()
        # 间隔 Tab
        self.interval_tab = QWidget()
        interval_layout = QVBoxLayout()
        interval_layout.addWidget(QLabel("每隔几分钟提醒："))
        self.input_minutes = QLineEdit()
        self.input_minutes.setValidator(QIntValidator(1, 1440, self))
        self.input_minutes.setPlaceholderText("例如 30")
        interval_layout.addWidget(self.input_minutes)
        interval_layout.addWidget(QLabel("提醒标题："))
        self.input_interval_title = QLineEdit()
        self.input_interval_title.setPlaceholderText("例如：休息提醒")
        interval_layout.addWidget(self.input_interval_title)
        interval_layout.addWidget(QLabel("提醒内容："))
        self.input_message = QLineEdit()
        self.input_message.setPlaceholderText("例如：起来活动一下~")
        interval_layout.addWidget(self.input_message)
        self.add_interval_btn = QPushButton("添加/保存间隔提醒")
        self.add_interval_btn.clicked.connect(self.on_add_interval_clicked)
        interval_layout.addWidget(self.add_interval_btn)
        interval_layout.addWidget(QLabel("间隔提醒列表："))
        self.interval_list = QListWidget()
        interval_layout.addWidget(self.interval_list)
        # 删除/修改
        btn1 = QHBoxLayout()
        self.edit_interval_btn = QPushButton("修改选中提醒")
        self.delete_interval_btn = QPushButton("删除选中提醒")
        self.edit_interval_btn.clicked.connect(self.handle_edit_interval)
        self.delete_interval_btn.clicked.connect(self.handle_delete_interval)
        btn1.addWidget(self.edit_interval_btn)
        btn1.addWidget(self.delete_interval_btn)
        interval_layout.addLayout(btn1)
        self.interval_tab.setLayout(interval_layout)
        # 每日 Tab
        self.daily_tab = QWidget()
        daily_layout = QVBoxLayout()
        time_layout = QHBoxLayout()
        time_layout.addStretch()
        self.input_hour = QLineEdit()
        self.input_hour.setValidator(QIntValidator(0,23,self))
        self.input_hour.setFixedWidth(50)
        self.input_hour.setPlaceholderText("08")
        time_layout.addWidget(self.input_hour)
        time_layout.addWidget(QLabel(":"),)
        self.input_minute = QLineEdit()
        self.input_minute.setValidator(QIntValidator(0,59,self))
        self.input_minute.setFixedWidth(50)
        self.input_minute.setPlaceholderText("00")
        time_layout.addWidget(self.input_minute)
        time_layout.addStretch()
        daily_layout.addLayout(time_layout)
        daily_layout.addWidget(QLabel("提醒标题："))
        self.input_daily_title = QLineEdit()
        self.input_daily_title.setPlaceholderText("例如：早餐提醒")
        daily_layout.addWidget(self.input_daily_title)
        daily_layout.addWidget(QLabel("提醒内容："))
        self.daily_message = QLineEdit()
        self.daily_message.setPlaceholderText("例如：早餐时间~")
        daily_layout.addWidget(self.daily_message)
        self.add_daily_btn = QPushButton("添加/保存每日提醒")
        self.add_daily_btn.clicked.connect(self.on_add_daily_clicked)
        daily_layout.addWidget(self.add_daily_btn)
        daily_layout.addWidget(QLabel("每日提醒列表："))
        self.daily_list = QListWidget()
        daily_layout.addWidget(self.daily_list)
        btn2 = QHBoxLayout()
        self.edit_daily_btn = QPushButton("修改选中提醒")
        self.delete_daily_btn = QPushButton("删除选中提醒")
        self.edit_daily_btn.clicked.connect(self.handle_edit_daily)
        self.delete_daily_btn.clicked.connect(self.handle_delete_daily)
        btn2.addWidget(self.edit_daily_btn)
        btn2.addWidget(self.delete_daily_btn)
        daily_layout.addLayout(btn2)
        self.daily_tab.setLayout(daily_layout)
        # 添加 tabs
        self.tabs.addTab(self.interval_tab, "间隔提醒")
        self.tabs.addTab(self.daily_tab, "每日提醒")
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

    def on_add_interval_clicked(self):
        title = self.input_interval_title.text().strip()
        minutes = self.input_minutes.text().strip()
        message = self.input_message.text().strip()
        if not (title and minutes and message):
            QMessageBox.warning(self, "错误", "请填写完整信息")
            return
        minutes = int(minutes)

        # —— 保存修改逻辑开始 —— #
        if self.editing_interval_id:
            # 1) 停掉旧任务
            remove_reminder(self.editing_interval_id)

            # 2) 从列表和字典里摘掉
            self.remove_list_item(self.interval_list, self.editing_interval_id)
            self.interval_tasks.pop(self.editing_interval_id)
            old_id = self.editing_interval_id
            self.editing_interval_id = None

            # 3) 新建任务并把 new_id 写回原来的提醒记录里
            new_id = add_interval_reminder(minutes, title, message)
            self.interval_tasks[new_id] = {'title': ...,
                                           'message': ...,
                                           'minutes': ...,
                                           'job_id': new_id}

            # 4) 更新那个列表项的 userRole，从 old_id 换成 new_id
            item = QListWidgetItem(f"[{title}] 每 {minutes} 分钟：{message}")
            item.setData(Qt.UserRole, new_id)
            self.interval_list.addItem(item)

            # 清除编辑状态
            self.editing_interval_id = None
            self.add_interval_btn.setText("添加/保存间隔提醒")
            return
        # —— 保存修改逻辑结束 —— #

        # 如果不是在编辑，就走“新增”分支
        job_id = add_interval_reminder(minutes, title, message)
        self.interval_tasks[job_id] = {
            'title': title,
            'message': message,
            'minutes': minutes,
            'job_id': job_id
        }
        item = QListWidgetItem(f"[{title}] 每 {minutes} 分钟：{message}")
        item.setData(Qt.UserRole, job_id)
        self.interval_list.addItem(item)

    def on_add_daily_clicked(self):
        title = self.input_daily_title.text().strip()
        hour = self.input_hour.text().strip()
        minute = self.input_minute.text().strip()
        message = self.daily_message.text().strip()
        if not (title and hour and minute and message):
            QMessageBox.warning(self, "错误", "请填写完整信息")
            return
        hour, minute = int(hour), int(minute)
        if self.editing_daily_id:
            # 1) 停掉旧任务
            old_id = self.editing_daily_id
            remove_reminder(old_id)

            # 2) 在内存中更新这条提醒的配置
            reminder = self.daily_tasks.pop(old_id)
            reminder['title'] = title
            reminder['message'] = message
            reminder['minutes'] = minute

            # 3) 重新添加新的任务
            new_id = add_daily_reminder(hour, minute, title, message,)
            reminder['job_id'] = new_id

            # 4) 更新字典键：用新 job_id 作为键
            self.daily_tasks[new_id] = reminder

            # 5) 更新列表项文本
            #    先找到原来的列表行，然后改它的 text() 和 UserRole 数据
            for i in range(self.daily_list.count()):
                item = self.daily_list.item(i)
                if item.data(Qt.UserRole) == old_id:
                    item.setText(f"[{title}] 每天 {hour:02d}:{minute:02d}：{message}")
                    item.setData(Qt.UserRole, new_id)
                    break

            # 5) 更新列表项文本
            #    先找到原来的列表行，然后改它的 text() 和 UserRole 数据
            for i in range(self.daily_list.count()):
                item = self.daily_list.item(i)
                if item.data(Qt.UserRole) == old_id:
                    item.setText(f"[{title}] 每天 {hour:02d}:{minute:02d}：{message}")
                    item.setData(Qt.UserRole, new_id)
                    break

            # 清除编辑状态
            self.editing_daily_id = None
            self.add_daily_btn.setText("添加/保存每日提醒")
            return
        # —— 保存修改逻辑结束 —— #

        # 如果不是在编辑，就走“新增”分支
        job_id = add_daily_reminder(hour, minute, title, message)
        self.daily_tasks[job_id] = {'title': title, 'message': message, 'hour': hour, 'minute': minute,  'job_id': job_id}

        item = QListWidgetItem(f"[{title}] 每天 {hour:02d}:{minute:02d}：{message}")
        item.setData(Qt.UserRole, job_id)
        self.daily_list.addItem(item)

    def handle_delete_interval(self):
        item = self.interval_list.currentItem()
        if not item:
            QMessageBox.warning(self, "错误", "请先选中一个任务")
            return
        job_id = item.data(Qt.UserRole)
        remove_reminder(job_id)  # ← 改为调用 remove_reminder
        row = self.interval_list.row(item)
        self.interval_list.takeItem(row)
        self.interval_tasks.pop(job_id, None)

    def handle_edit_interval(self):
        item = self.interval_list.currentItem()
        if not item:
            QMessageBox.warning(self, "错误", "请先选中一个任务")
            return
        job_id = item.data(Qt.UserRole)
        data = self.interval_tasks[job_id]
        # 回填并进入编辑模式
        self.input_interval_title.setText(data['title'])
        self.input_minutes.setText(str(data['minutes']))
        self.input_message.setText(data['message'])
        self.editing_interval_id = job_id
        # 切回 Tab，提示保存
        self.tabs.setCurrentWidget(self.interval_tab)
        self.add_interval_btn.setText("保存修改")

    def handle_delete_daily(self):
        item = self.daily_list.currentItem()
        if not item:
            QMessageBox.warning(self, "错误", "请先选中一个任务")
            return
        job_id = item.data(Qt.UserRole)
        remove_reminder(job_id)
        row = self.daily_list.row(item)
        self.daily_list.takeItem(row)
        self.daily_tasks.pop(job_id, None)

    def handle_edit_daily(self):
        item = self.daily_list.currentItem()
        if not item:
            QMessageBox.warning(self, "错误", "请先选中一个任务")
            return
        job_id = item.data(Qt.UserRole)
        data = self.daily_tasks[job_id]
        self.input_daily_title.setText(data['title'])
        self.input_hour.setText(str(data['hour']))
        self.input_minute.setText(str(data['minute']))
        self.daily_message.setText(data['message'])
        self.editing_daily_id = job_id
        self.tabs.setCurrentWidget(self.daily_tab)
        self.add_daily_btn.setText("保存修改")

    def remove_list_item(self, list_widget, job_id):
        for i in range(list_widget.count()):
            item = list_widget.item(i)
            if item.data(Qt.UserRole) == job_id:
                list_widget.takeItem(i)
                return