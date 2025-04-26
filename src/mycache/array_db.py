import sqlite3
import numpy as np
import io
import os

if not os.path.exists("save"):
    os.makedirs("save")

TABLE_NAME = "array_data"
SAVE_DB_PATH = "save/array_data.db"


def save_array_to_db(key: str, array: np.ndarray) -> None:
    """NumPy配列をSQLiteデータベースに保存する"""

    # NumPy配列をバイナリに変換
    array_bytes = io.BytesIO()
    np.save(array_bytes, array)
    array_bytes = array_bytes.getvalue()

    # データベース接続・テーブル作成
    conn = sqlite3.connect(SAVE_DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id TEXT PRIMARY KEY,
            array_data BLOB
        )
    """
    )

    # データを挿入または置換
    cursor.execute(
        f"""
        INSERT OR REPLACE INTO {TABLE_NAME} (id, array_data) VALUES (?, ?)
    """,
        (key, array_bytes),
    )

    conn.commit()
    conn.close()


def load_array_from_db(key: str) -> np.ndarray:
    """SQLiteデータベースからNumPy配列を読み込む"""
    conn = sqlite3.connect(SAVE_DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        f"""
        SELECT array_data FROM {TABLE_NAME} WHERE id=?
    """,
        (key,),
    )
    result = cursor.fetchone()
    conn.close()

    if result is None:
        raise KeyError(f"No entry found for key: {key}")

    # バイナリデータからNumPy配列に復元
    array_bytes = io.BytesIO(result[0])
    array = np.load(array_bytes, allow_pickle=True)
    return array
