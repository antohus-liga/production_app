from PySide6.QtSql import QSqlDatabase
from sql.db_initializer import db_path, initialize_schema


def get_connection():
    initialize_schema()

    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(db_path)
    if not db.open():
        print("Could not open the database")
        exit()

    return db
