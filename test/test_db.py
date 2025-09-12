import os
import database

def test_connection():
    # 检查数据库文件路径
    db_path = os.path.abspath(database.DB_FILE)
    print(f"数据库文件位置: {db_path}")
    try:
        conn = database.get_connection()
        cursor = conn.cursor()
        # 列出所有表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        print("已连接数据库，发现表:", tables)
        # 尝试读取已有记录
        from database import load_all
        records = load_all()
        print(f"load_all() 返回 {len(records)} 条记录：")
        for rec in records:
            print(rec)
    except Exception as e:
        print("连接或查询数据库时出错：", e)
    finally:
        conn.close()

if __name__ == "__main__":
    test_connection()
