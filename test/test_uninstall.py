import os

def remove_startup_registry_entry():
    print("模拟删除注册表启动项（不实际删除）")

def confirm_and_delete_dir():
    current_dir = os.path.abspath(os.path.dirname(__file__))
    print(f"📂 当前程序目录为：\n  {current_dir}")
    confirm = input("⚠️ 确认删除该目录及其所有内容？(yes/no): ").strip().lower()
    if confirm == "yes":
        print(f"模拟删除目录：{current_dir} （实际未执行删除）")
    else:
        print("❎ 已取消删除。")

if __name__ == "__main__":
    remove_startup_registry_entry()
    confirm_and_delete_dir()
