import psycopg2
from psycopg2.extras import RealDictCursor

class Database:
    def __init__(self, db_config):
        """Инициализация подключения к базе данных."""
        try:
            self.conn = psycopg2.connect(**db_config)
            self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        except Exception as e:
            print(f"Ошибка подключения к базе данных: {e}")
            raise

    def execute(self, query, params=None):
        """Выполнение SQL-запроса без возврата результата."""
        try:
            self.cursor.execute(query, params or ())
            self.conn.commit()
        except Exception as e:
            print(f"Ошибка выполнения запроса: {query} \n{e}")
            self.conn.rollback()
            raise

    def fetchall(self, query, params=None):
        """Получение всех строк результата SQL-запроса."""
        self.cursor.execute(query, params or ())
        return self.cursor.fetchall()

    def fetchone(self, query, params=None):
        """Получение одной строки результата SQL-запроса."""
        self.cursor.execute(query, params or ())
        return self.cursor.fetchone()

    def commit(self):
        """Фиксация изменений."""
        try:
            self.conn.commit()
        except Exception as e:
            print(f"Ошибка при коммите: {e}")
            raise

    def close(self):
        """Закрытие подключения к базе данных."""
        try:
            self.cursor.close()
            self.conn.close()
        except Exception as e:
            print(f"Ошибка при закрытии соединения: {e}")