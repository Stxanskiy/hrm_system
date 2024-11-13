from PyQt6.QtWidgets import QApplication
from db.database import Database
from hrm_system.auth import Auth

DB_CONFIG = {
    'dbname': 'hrm_system',
    'user': 'postgres',
    'password': '456456',
    'host': 'localhost',
    'port': 5432
}

def main():
    db = Database(DB_CONFIG)
    app = QApplication([])
    auth_window = Auth(db)
    auth_window.show()
    app.exec()

if __name__ == "__main__":
    main()
