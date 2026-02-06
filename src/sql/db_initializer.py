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
        CREATE TABLE IF NOT EXISTS suppliers(
            code TEXT PRIMARY KEY NOT NULL,
            first_name TEXT,
            last_name TEXT,
            sup_type TEXT,
            company_name TEXT,
            country TEXT,
            city TEXT,
            phone TEXT,
            email TEXT,
            date_of_birth DATE,
            nif TEXT,
            created_at TEXT,
            updated_at TEXT
        );
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS clients(
            code TEXT PRIMARY KEY NOT NULL,
            first_name TEXT,
            last_name TEXT,
            cli_type TEXT,
            company_name TEXT,
            country TEXT,
            city TEXT,
            phone TEXT,
            email TEXT,
            date_of_birth DATE,
            nif TEXT,
            created_at TEXT,
            updated_at TEXT
        );
        """
    )

    # quantity IS CALCULATED
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS materials(
            code TEXT PRIMARY KEY NOT NULL,
            name TEXT,
            category TEXT,
            base_unit TEXT,
            unit_price FLOAT NOT NULL DEFAULT 0,
            quantity INTEGER NOT NULL DEFAULT 0,
            created_at TEXT,
            updated_at TEXT
        );
        """
    )

    # quantity IS CALCULATED
    # production_cost IS CALCULATED
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS products(
            code TEXT PRIMARY KEY NOT NULL,
            name TEXT,
            category TEXT,
            base_unit TEXT,
            unit_price FLOAT NOT NULL DEFAULT 0,
            quantity INTEGER NOT NULL DEFAULT 0,
            production_cost FLOAT NOT NULL DEFAULT 0,
            created_at TEXT,
            updated_at TEXT
        );
        """
    )

    # total_price IS CALCULATED
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS movements_in(
            nr INTEGER PRIMARY KEY AUTOINCREMENT,
            mat_code TEXT,
            sup_code TEXT,
            quantity INTEGER NOT NULL DEFAULT 0,
            total_price FLOAT NOT NULL DEFAULT 0,
            created_at TEXT,
            updated_at TEXT,
            FOREIGN KEY(mat_code) REFERENCES materials(code),
            FOREIGN KEY(sup_code) REFERENCES suppliers(code)
        );
        """
    )

    # total_price IS CALCULATED
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS movements_out(
            nr INTEGER PRIMARY KEY AUTOINCREMENT,
            pro_code TEXT,
            cli_code TEXT,
            quantity INTEGER NOT NULL DEFAULT 0,
            total_price FLOAT NOT NULL DEFAULT 0,
            created_at TEXT,
            updated_at TEXT,
            FOREIGN KEY(pro_code) REFERENCES products(code),
            FOREIGN KEY(cli_code) REFERENCES clients(code)
        );
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS product_materials(
            nr INTEGER PRIMARY KEY AUTOINCREMENT,
            pro_code TEXT,
            mat_code TEXT,
            quantity INTEGER NOT NULL DEFAULT 0,
            CONSTRAINT uq_pro_mat UNIQUE (pro_code, mat_code),
            FOREIGN KEY(pro_code) REFERENCES materials(code),
            FOREIGN KEY(mat_code) REFERENCES supliers(code)
        );
        """
    )

    # total_cost IS CALCULATED
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS production_line(
            nr INTEGER PRIMARY KEY AUTOINCREMENT,
            pro_code TEXT,
            quantity INTEGER NOT NULL DEFAULT 0,
            total_cost FLOAT NOT NULL DEFAULT 0,
            created_at TEXT,
            updated_at TEXT,
            FOREIGN KEY(pro_code) REFERENCES products(code)
        );
        """
    )

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
