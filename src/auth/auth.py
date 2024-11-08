import hashlib
import psycopg2

class Auth:
    def __init__(self, db_config):
        try:
            self.conn = psycopg2.connect(**db_config)
            self.cur = self.conn.cursor()
            print("Соединение с базой данных установлено.")
        except psycopg2.OperationalError as e:
            print(f"Не удалось подключиться к базе данных: {e}")
            raise

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, username, password, role):
        hashed_password = self.hash_password(password)
        self.cur.execute(
            "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
            (username, hashed_password, role)
        )
        self.conn.commit()

    def login(self, username, password, role):
        hashed_password = self.hash_password(password)
        self.cur.execute(
            "SELECT * FROM users WHERE username = %s AND password = %s AND role = %s",
            (username, hashed_password, role)
        )
        return self.cur.fetchone() is not None
