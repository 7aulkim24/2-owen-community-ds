from typing import Any, Dict, Iterable, Optional, Tuple
from mysql.connector.pooling import MySQLConnectionPool
from config import settings


_pool = MySQLConnectionPool(
    pool_name="community_pool",
    pool_size=settings.db_pool_size,
    host=settings.db_host,
    port=settings.db_port,
    user=settings.db_user,
    password=settings.db_password,
    database=settings.db_name,
    autocommit=False,
)


def _execute(
    query: str,
    params: Optional[Iterable[Any]] = None,
    fetchone: bool = False,
    fetchall: bool = False,
) -> Any:
    conn = _pool.get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query, params or ())
        result = None
        if fetchone:
            result = cursor.fetchone()
        elif fetchall:
            result = cursor.fetchall()
        conn.commit()
        return result
    finally:
        cursor.close()
        # MySQL 커넥션 풀에서는 close() 호출 시 실제 연결이 닫히지 않고 풀에 반환됨
        conn.close()


def fetch_one(query: str, params: Optional[Iterable[Any]] = None) -> Optional[Dict[str, Any]]:
    return _execute(query, params=params, fetchone=True)


def fetch_all(query: str, params: Optional[Iterable[Any]] = None) -> Iterable[Dict[str, Any]]:
    return _execute(query, params=params, fetchall=True)


def execute(query: str, params: Optional[Iterable[Any]] = None) -> int:
    conn = _pool.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params or ())
        conn.commit()
        return cursor.rowcount
    finally:
        cursor.close()
        # MySQL 커넥션 풀에서는 close() 호출 시 실제 연결이 닫히지 않고 풀에 반환됨
        conn.close()
