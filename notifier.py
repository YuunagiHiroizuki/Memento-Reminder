# notifier.py
import os
import sys
import winsound
from winotify import Notification

def show_notification(title: str, message: str):
    toast = Notification(
        app_id="Reminder",
        title=title,
        msg=message,
        duration="short"
    )
    toast.show()

    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        sound_path = os.path.join(base_dir, "sounds", "alert.wav")
        if os.path.exists(sound_path):
            winsound.PlaySound(sound_path, winsound.SND_FILENAME)
        else:
            print(f"[警告] 找不到音效文件: {sound_path}")
    except Exception as e:
        print(f"[错误] 播放音效时出错: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python notifier.py <标题> <内容>")
    else:
        title = sys.argv[1]
        message = sys.argv[2]
        show_notification(title, message)
