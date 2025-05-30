# database.py
import os
import sqlite3
import uuid

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)
DB_FILE = os.path.join(DATA_DIR, "reminders.db")

def get_connection():
    return sqlite3.connect(DB_FILE)

def init_db():
    """创建 reminders 表（只需在程序启动时执行一次）"""
    with get_connection() as conn:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS reminders (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            message TEXT NOT NULL,
            mode TEXT NOT NULL,           -- 'interval' or 'daily'
            interval_min INTEGER,         -- 仅 mode='interval' 有意义
            time TEXT,                    -- 'HH:MM' 仅 mode='daily' 有意义
            enabled INTEGER NOT NULL      -- 1=启用, 0=禁用
        )
        ''')
        conn.commit()

def add_interval(title: str, message: str, minutes: int) -> str:
    rid = str(uuid.uuid4())
    with get_connection() as conn:
        conn.execute('''
            INSERT INTO reminders (id,title,message,mode,interval_min,time,enabled)
            VALUES (?, ?, ?, 'interval', ?, NULL, 1)
        ''', (rid, title, message, minutes))
        conn.commit()
    return rid

def add_daily(title: str, message: str, hhmm: str) -> str:
    rid = str(uuid.uuid4())
    with get_connection() as conn:
        conn.execute('''
            INSERT INTO reminders (id,title,message,mode,interval_min,time,enabled)
            VALUES (?, ?, ?, 'daily', NULL, ?, 1)
        ''', (rid, title, message, hhmm))
        conn.commit()
    return rid

def delete_reminder(rid: str):
    with get_connection() as conn:
        conn.execute('DELETE FROM reminders WHERE id = ?', (rid,))
        conn.commit()

def update_interval(rid: str, title: str, message: str, minutes: int):
    with get_connection() as conn:
        conn.execute('''
            UPDATE reminders
               SET title=?, message=?, interval_min=?
             WHERE id=? AND mode='interval'
        ''', (title, message, minutes, rid))
        conn.commit()

def update_daily(rid: str, title: str, message: str, hhmm: str):
    with get_connection() as conn:
        conn.execute('''
            UPDATE reminders
               SET title=?, message=?, time=?
             WHERE id=? AND mode='daily'
        ''', (title, message, hhmm, rid))
        conn.commit()

def load_all() -> list[dict]:
    """载入所有启用的提醒记录，返回字典列表"""
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute('SELECT id,title,message,mode,interval_min,time FROM reminders WHERE enabled=1')
        rows = cur.fetchall()
    result = []
    for id_, t, m, mode, iv, tm in rows:
        result.append({
            'id':       id_,
            'title':    t,
            'message':  m,
            'mode':     mode,
            'interval': iv,
            'time':     tm
        })
    return result
