import os

from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon

class SystemTray(QSystemTrayIcon):
    def __init__(self, icon_path, parent_window=None):
        super(SystemTray, self).__init__()
        self.parent_window = parent_window

        # 加载图标
        base_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base_dir, "icon", "memento.ico")
        self.setIcon(QIcon(icon_path))

        # 菜单
        self.menu = QMenu()

        self.show_action = QAction("显示窗口")
        self.show_action.triggered.connect(self.show_main_window)
        self.menu.addAction(self.show_action)

        self.setting_action = QAction("设置", self)
        self.setting_action.triggered.connect(self.show_setting_tab)
        self.menu.addAction(self.setting_action)

        self.quit_action = QAction("退出程序")
        self.quit_action.triggered.connect(self.exit_app)
        self.menu.addAction(self.quit_action)

        self.setContextMenu(self.menu)
        self.setToolTip("Memento")
        self.show()

        # 点击图标时显示主界面
        self.activated.connect(self.on_click)

        # 显示托盘
        self.show()

    def show_main_window(self):
        self.parent_window.show()
        self.parent_window.raise_()
        self.parent_window.activateWindow()

    def show_setting_tab(self):
        if not self.parent_window.isVisible():
            self.parent_window.showNormal()
            self.parent_window.activateWindow()
        # 切换到“设置”标签页
        self.parent_window.tabs.setCurrentIndex(2)

    def exit_app(self):
        self.setVisible(False)  # 隐藏托盘图标
        QApplication.quit()     # 退出应用主循环

    def on_click(self, reason):
        if reason == QSystemTrayIcon.Trigger:  # 单击图标
            if self.parent_window.isVisible():
                self.parent_window.hide()
            else:
                self.parent_window.showNormal()
                self.parent_window.activateWindow()