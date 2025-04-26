import sqlite3
import hashlib
import pickle
import inspect
import functools
import sys
import os
import tempfile

if not os.path.exists("cache"):
    os.makedirs("cache")


# SQLiteデータベースの初期化


if "pytest" in sys.modules:
    DB_PATH = "cache/test.db"
else:
    DB_PATH = "cache/cache.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
cur.execute(
    """
CREATE TABLE IF NOT EXISTS cache (
    func_name TEXT,
    func_hash TEXT,
    args_hash TEXT,
    result BLOB,
    PRIMARY KEY (func_name, func_hash, args_hash)
)
"""
)
conn.commit()


def cache_to_sqlite(func):
    func_name = func.__name__
    # 関数のソースコードからハッシュを作成
    func_code = inspect.getsource(func)
    func_hash = hashlib.sha256(func_code.encode("utf-8")).hexdigest()

    @functools.wraps(func)
    def wrapper(*args: tuple, **kwargs: dict) -> object:
        # 引数をハッシュ化
        args_key = pickle.dumps((args, kwargs))
        args_hash = hashlib.sha256(args_key).hexdigest()

        # キャッシュをチェック
        cur.execute(
            """
            SELECT result FROM cache WHERE func_name=? AND func_hash=? AND args_hash=?
        """,
            (func_name, func_hash, args_hash),
        )
        row = cur.fetchone()
        if row:
            return pickle.loads(row[0])

        # 計算してキャッシュに保存
        result = func(*args, **kwargs)
        cur.execute(
            """
            INSERT OR REPLACE INTO cache (func_name, func_hash, args_hash, result)
            VALUES (?, ?, ?, ?)
        """,
            (func_name, func_hash, args_hash, pickle.dumps(result)),
        )
        conn.commit()
        return result

    return wrapper
