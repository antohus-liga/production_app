import os
import sqlite3


db_path = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "appdata",
    "production_info.db",
)


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(db_path)
    return connection


def initialize_schema() -> None:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TRIGGER IF NOT EXISTS trg_products_quantity_non_negative
        BEFORE UPDATE OF quantity ON products
        FOR EACH ROW
        WHEN NEW.quantity < 0
        BEGIN
            SELECT RAISE(ABORT, 'Quantidade de materiais insuficiente.');
        END;
        """
    )

    cursor.execute(
        """
        CREATE TRIGGER IF NOT EXISTS trg_materials_quantity_non_negative
        BEFORE UPDATE OF quantity ON materials
        FOR EACH ROW
        WHEN NEW.quantity < 0
        BEGIN
            SELECT RAISE(ABORT, 'Quantidade de materiais insuficiente.');
        END;
        """
    )

    connection.commit()
    connection.close()
