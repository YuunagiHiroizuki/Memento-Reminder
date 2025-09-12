# 📝 Memento — 定时提醒工具
 pyinstaller main.py --name Memento --noconfirm --windowed --icon=icon/memento.ico --add-data "icon/memento.ico;icon" --add-data "sounds/reminder.wav;sounds" --add-data "data/memento.db;data"
没打包好，TODO的测试用计时忘改了，而且打包后还没有unistall.py得自己加进去
## 🎯 项目简介
本项目是一个用于定时提醒用户休息的工具，目标是在不打扰用户当前工作的前提下，通过 Windows 消息中心或系统托盘提醒长时间坐在电脑前的用户起身活动。项目采用 Python 开发，使用 PyQt5 构建 GUI， QTimer 实现定时任务调度，提醒信息持久化保存至 JSON 文件。

---

✅ 项目依赖（requirements.txt）
txt
复制
编辑
PyQt5>=5.15
winotify>=0.2
APScheduler>=3.10

## 🔧 技术栈与依赖

- **语言**：Python 3.x  
- **主要库**：
  - `PyQt5`：图形界面与系统托盘
  - `QtScheduler+QTimer`：任务调度器
  - `win10toast` / `plyer` / Windows 消息中心：提醒弹窗
  - `matplotlib`（可选）：数据可视化
- **数据持久化**：JSON 文件（必要，课程要求）
- **可选**：SQLite（若转为复杂查询或待办事项管理）
# 项目未来规划
- 若引入更多可自定义设置项（如通知音、界面主题等），将采用 `settings.json` 存储配置。
- 使用QTDesigner设计更简约现代的界面
---

## ✅ 主要功能一览（优先级标记）

| 功能                     | 描述                        | 优先级        |
|------------------------|---------------------------|------------|
| 间隔提醒                   | 每隔指定时间弹窗提醒                | ★★★★★ ✅已完成 |
| 指定时间提醒                 | 在某一指定时间弹窗提醒               | ★★★★☆ ✅已完成 |
| 添加/修改/删除提醒任务           | GUI 操作任务内容（基于 ID）         | ★★★☆☆ ✅已完成 |
| 提醒任务保存读取               | 使用 SQLite 保存任务            | ★★★★☆ ✅已完成 |
| 系统托盘支持                 | 使用 `QSystemTrayIcon` 托盘运行 | ★★☆☆☆ ✅已完成 |
| Deadline 倒计时**/待办事项显示* | 可选功能，不做不影响主体              | ★☆☆☆☆ 可选   |

---

## ✅ 开发优先顺序建议

1. **提醒引擎开发**：  
   QtScheduler + QTimer + Windows 消息中心弹窗（核心功能）

2. **任务管理逻辑**：  
   ReminderTask 类、ReminderManager 类封装逻辑（OOP结构）

3. **任务保存读取功能**：  
   使用 JSON 文件进行任务增删改查持久化

4. **GUI 界面开发**：  
   简洁清晰的增删改提醒任务界面（PyQt5）

5. **系统托盘功能**：  
   实现最小化到托盘、托盘菜单、退出按钮等,ICON

6. **（可选）Deadline 与待办事项功能**：  
   若时间充裕再实现

---

## 🎁 可选进阶功能（视时间决定）

- 自定义提醒内容 ✅
- 开机自启（注册表或任务计划程序）
- 简单数据可视化（matplotlib 柱状图展示提醒频率）

---

## 🧠 面向对象设计建议

- `ReminderTask`：代表一个提醒任务（含任务ID、类型、时间、间隔等）
- `ReminderManager`：统一管理任务的添加、修改、删除、保存、加载
- GUI层控制与数据层解耦

---

