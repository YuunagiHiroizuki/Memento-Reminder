# Windows消息弹窗封装（winotify）
import os

import winsound
from winotify import Notification

def show_notification(title: str, message: str):
    """
    展示 Windows 系统通知 + 播放提示音
    参数：
    - message: 提醒的正文内容
    - title: 提醒的标题，默认为“定时提醒”
    """
    toast = Notification(
        app_id="Reminder",
        title=title,
        msg=message,
        duration="short"
    )
    #显示通知气泡
    toast.show()
    #播放提示音
    try:
        # 获取当前脚本所在目录
        base_dir = os.path.dirname(os.path.abspath(__file__))
        sound_path = os.path.join(base_dir, "sounds", "alert.wav")

        if os.path.exists(sound_path):
            winsound.PlaySound(sound_path, winsound.SND_FILENAME)
        else:
            print(f"[警告] 找不到音效文件: {sound_path}")
    except Exception as e:
        print(f"[错误] 播放音效时出错: {e}")
