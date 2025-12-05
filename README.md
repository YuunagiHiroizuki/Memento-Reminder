# Memento — 定时提醒工具

Python 3.x 
Use PyQt5 + QtScheduler+ QTimer + win10toast/plyer

## 项目说明

本项目是一个用于定时提醒用户休息的工具，目标是在不打扰用户当前工作的前提下，通过 Windows 消息中心或系统托盘提醒长时间坐在电脑前的用户起身活动。项目采用 Python 开发，使用 PyQt5 构建 GUI， QTimer 实现定时任务调度，数据持久化保存至SQLite。

---

##项目依赖（requirements.txt）

PyQt5>=5.15
winotify>=0.2
APScheduler>=3.10

## 打包

```bash
pyinstaller main.py --name Memento --noconfirm --windowed --icon=icon/memento.ico --add-data "icon/memento.ico;icon" --add-data "sounds/reminder.wav;sounds" --add-data "data/memento.db;data"
```
打包后需要将unistall.py手动添加到项目根目录

## 未来拓展

- 若引入更多可自定义设置项（如通知音、界面主题等），将采用 `settings.json` 存储配置。
- 使用Eletron替代PyQt5

---

## 主要功能

| 功能                     | 描述                        | 
|------------------------|---------------------------|------------|
| 间隔提醒                   | 每隔指定时间弹窗提醒                |
| 指定时间提醒                 | 在某一指定时间弹窗提醒               |
| 添加/修改/删除提醒任务           | GUI 操作任务内容（基于 ID）         |
| 提醒任务保存读取               | 使用 SQLite 保存任务            |
| 系统托盘支持                 | 使用 `QSystemTrayIcon` 托盘运行 |  

---
 
1. **提醒引擎**：  
   QtScheduler + QTimer + Windows 消息中心弹窗（核心功能）

2. **任务管理逻辑**：  
   ReminderTask 类、ReminderManager 类封装逻辑（OOP结构）

3. **任务保存读取**：  
   使用 JSON 文件进行任务增删改查持久化

4. **GUI 界面**：  
   简洁清晰的增删改提醒任务界面（PyQt5）

5. **系统托盘功能**：  
   实现最小化到托盘、托盘菜单、退出按钮等,ICON

6. **开机自启（注册表或任务计划程序）**

7. **附带删除程序**
