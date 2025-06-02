import sys
import winreg
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QTabWidget, QListWidget, QListWidgetItem, QDialog, QCheckBox
)
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt

class ReminderGUI(QWidget):
    def __init__(self, mgr):
        super().__init__()
        self.mgr = mgr  # ReminderManager instance
        self.setWindowTitle("Memento")
        self.setFixedSize(400, 450)
        self.editing_interval_id = None
        self.editing_daily_id = None
        self.interval_tasks = {}  # id->meta
        self.daily_tasks = {}
        self.setup_ui()
        self.load_existing()

    def load_existing(self):
        for rec in self.mgr.load_all():
            if rec['mode'] == 'interval':
                self.add_interval_item(
                    rec['id'], rec['title'], rec['message'], rec['interval']
                )
            else:
                h, m = map(int, rec['time'].split(':'))
                self.add_daily_item(
                    rec['id'], rec['title'], rec['message'], h, m
                )

    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        self.tabs = QTabWidget()
        # Interval Tab
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
        btn1 = QHBoxLayout()
        self.edit_interval_btn = QPushButton("修改选中提醒")
        self.delete_interval_btn = QPushButton("删除选中提醒")
        self.edit_interval_btn.clicked.connect(self.handle_edit_interval)
        self.delete_interval_btn.clicked.connect(self.handle_delete_interval)
        btn1.addWidget(self.edit_interval_btn)
        btn1.addWidget(self.delete_interval_btn)
        interval_layout.addLayout(btn1)
        self.interval_tab.setLayout(interval_layout)

        # Daily Tab
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

        #setting
        self.setting_tab = QWidget()
        layout = QVBoxLayout()
        # 创建复选框
        self.auto_start_checkbox = QCheckBox("开机启动")

        layout.addWidget(self.auto_start_checkbox, alignment=Qt.AlignLeft | Qt.AlignTop)
        # 设置复选框状态
        self.auto_start_checkbox.setChecked(self.is_auto_start_enabled())
        # 状态改变自动保存
        self.auto_start_checkbox.stateChanged.connect(self.on_auto_start_changed)

        self.setting_tab.setLayout(layout)


        self.tabs.addTab(self.interval_tab, "间隔提醒")
        self.tabs.addTab(self.daily_tab, "每日提醒")
        self.tabs.addTab(self.setting_tab, "设置")
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

    def load_existing(self):
        for rec in self.mgr.load_all():
            if rec['mode']=='interval':
                self.add_interval_item(rec['id'], rec['title'], rec['message'], rec['interval'])
            else:
                hh, mm = map(int, rec['time'].split(':'))
                self.add_daily_item(rec['id'], rec['title'], rec['message'], hh, mm)

    def add_interval_item(self, rid, title, message, minutes):
        item = QListWidgetItem(f"[{title}] 每 {minutes} 分钟：{message}")
        item.setData(Qt.UserRole, rid)
        self.interval_list.addItem(item)
        self.interval_tasks[rid] = {'title':title,'message':message,'minutes':minutes}

    def add_daily_item(self, rid, title, message, hh, mm):
        item = QListWidgetItem(f"[{title}] 每天 {hh:02d}:{mm:02d}：{message}")
        item.setData(Qt.UserRole, rid)
        self.daily_list.addItem(item)
        self.daily_tasks[rid] = {'title':title,'message':message,'hour':hh,'minute':mm}

    def on_add_interval_clicked(self):
        title = self.input_interval_title.text().strip()
        mins  = self.input_minutes.text().strip()
        msg   = self.input_message.text().strip()
        if not(title and mins and msg):
            QMessageBox.warning(self, "错误", "请填写完整信息")
            return
        minutes=int(mins)
        if self.editing_interval_id:
            rid = self.editing_interval_id
            self.mgr.modify_interval(rid, title, msg, minutes)
            self.update_list_item(self.interval_list, rid, f"[{title}] 每 {minutes} 分钟：{msg}")
            self.editing_interval_id=None
            self.add_interval_btn.setText("添加/保存间隔提醒")
        else:
            rid=self.mgr.add_interval(title,msg,minutes)
            self.add_interval_item(rid,title,msg,minutes)

    def on_add_daily_clicked(self):
        title=self.input_daily_title.text().strip()
        hh=self.input_hour.text().strip(); mm=self.input_minute.text().strip()
        msg=self.daily_message.text().strip()
        if not(title and hh and mm and msg):
            QMessageBox.warning(self, "错误", "请填写完整信息")
            return
        hh,mm=int(hh),int(mm)
        if self.editing_daily_id:
            rid=self.editing_daily_id
            self.mgr.modify_daily(rid,title,msg,f"{hh:02d}:{mm:02d}")
            self.update_list_item(self.daily_list, rid, f"[{title}] 每天 {hh:02d}:{mm:02d}：{msg}")
            self.editing_daily_id=None
            self.add_daily_btn.setText("添加/保存每日提醒")
        else:
            rid=self.mgr.add_daily(title,msg,f"{hh:02d}:{mm:02d}")
            self.add_daily_item(rid,title,msg,hh,mm)

    def handle_delete_interval(self):
        item=self.interval_list.currentItem()
        if not item:
            QMessageBox.warning(self, "错误", "请先选中一个任务")
            return
        rid=item.data(Qt.UserRole)
        self.mgr.remove(rid)
        self.interval_list.takeItem(self.interval_list.row(item))
        self.interval_tasks.pop(rid,None)

    def handle_edit_interval(self):
        item=self.interval_list.currentItem()
        if not item:
            QMessageBox.warning(self, "错误", "请先选中一个任务")
            return
        rid=item.data(Qt.UserRole)
        data=self.interval_tasks[rid]
        self.input_interval_title.setText(data['title'])
        self.input_minutes.setText(str(data['minutes']))
        self.input_message.setText(data['message'])
        self.editing_interval_id=rid
        self.tabs.setCurrentWidget(self.interval_tab)
        self.add_interval_btn.setText("保存修改")

    def handle_delete_daily(self):
        item=self.daily_list.currentItem()
        if not item:
            QMessageBox.warning(self, "错误", "请先选中一个任务")
            return
        rid=item.data(Qt.UserRole)
        self.mgr.remove(rid)
        self.daily_list.takeItem(self.daily_list.row(item))
        self.daily_tasks.pop(rid,None)

    def handle_edit_daily(self):
        item=self.daily_list.currentItem()
        if not item:
            QMessageBox.warning(self, "错误", "请先选中一个任务")
            return
        rid=item.data(Qt.UserRole)
        data=self.daily_tasks[rid]
        self.input_daily_title.setText(data['title'])
        self.input_hour.setText(str(data['hour']))
        self.input_minute.setText(str(data['minute']))
        self.daily_message.setText(data['message'])
        self.editing_daily_id=rid
        self.tabs.setCurrentWidget(self.daily_tab)
        self.add_daily_btn.setText("保存修改")

    def update_list_item(self, list_w, rid, text):
        for i in range(list_w.count()):
            it=list_w.item(i)
            if it.data(Qt.UserRole)==rid:
                it.setText(text)
                return

    def show_settings(self):
        self.settings_dialog.exec_()

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def is_auto_start_enabled(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                 r"Software\Microsoft\Windows\CurrentVersion\Run",
                                 0, winreg.KEY_READ)
            val, _ = winreg.QueryValueEx(key, "Memento")
            return True
        except FileNotFoundError:
            return False

    def on_auto_start_changed(self, state):
        exe_path = sys.executable
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                 r"Software\Microsoft\Windows\CurrentVersion\Run",
                                 0, winreg.KEY_SET_VALUE)
            if state == 2:  # Checked
                winreg.SetValueEx(key, "Memento", 0, winreg.REG_SZ, exe_path)
            else:
                winreg.DeleteValue(key, "Memento")
        except FileNotFoundError:
            # 如果要删除的值不存在，忽略即可
            pass