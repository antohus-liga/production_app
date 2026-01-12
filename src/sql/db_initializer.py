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
            quantity INTEGER NOT NULL DEFAULT 0,
            base_unit TEXT,
            unit_price FLOAT NOT NULL DEFAULT 0,
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
            quantity INTEGER NOT NULL DEFAULT 0,
            base_unit TEXT,
            unit_price FLOAT NOT NULL DEFAULT 0,
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
            FOREIGN KEY(sup_code) REFERENCES supliers(code)
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
            FOREIGN KEY(pro_code) REFERENCES materials(code),
            FOREIGN KEY(cli_code) REFERENCES supliers(code)
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
            FOREIGN KEY(pro_code) REFERENCES materials(code)
        );
        """
    )

    connection.commit()
    connection.close()
