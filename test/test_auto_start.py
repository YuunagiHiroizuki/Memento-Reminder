import winreg

def is_auto_start_enabled():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r"Software\Microsoft\Windows\CurrentVersion\Run",
                             0, winreg.KEY_READ)
        val, _ = winreg.QueryValueEx(key, "Memento")
        print(f"开机启动路径: {val}")
        return True
    except FileNotFoundError:
        print("未设置开机启动")
        return False

is_auto_start_enabled()
