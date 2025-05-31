import os
import shutil
import sys
import winreg

def remove_startup_registry_entry():
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0, winreg.KEY_SET_VALUE
        )
        winreg.DeleteValue(key, "ReminderApp")
        print("✅ 启动项已从注册表中删除。")
    except FileNotFoundError:
        print("ℹ️ 注册表中未找到启动项，无需删除。")
    except Exception as e:
        print(f"❌ 删除注册表启动项失败: {e}")

def confirm_and_delete_dir():
    current_dir = os.path.abspath(os.path.dirname(__file__))
    print(f"📂 当前程序目录为：\n  {current_dir}")
    confirm = input("⚠️ 确认删除该目录及其所有内容？(yes/no): ").strip().lower()
    if confirm == "y":
        try:
            shutil.rmtree(current_dir)
            print("✅ 程序目录已删除。")
        except Exception as e:
            print(f"❌ 删除目录失败: {e}")
    else:
        print("❎ 已取消删除。")

if __name__ == "__main__":
    remove_startup_registry_entry()
    confirm_and_delete_dir()
