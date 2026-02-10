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

    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_movements_in_mat_code
        ON movements_in(mat_code);
        """
    )

    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_product_materials_mat_code
        ON product_materials(mat_code);
        """
    )

    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_product_materials_pro_code
        ON product_materials(pro_code);
        """
    )

    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_production_line_pro_code
        ON production_line(pro_code);
        """
    )

    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_movements_in_mat_code
        ON movements_in(mat_code);
        """
    )

    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_movements_in_mat_code
        ON movements_in(mat_code);
        """
    )

    connection.commit()
    connection.close()
