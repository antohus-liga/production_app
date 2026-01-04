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
            sup_id INTEGER PRIMARY KEY AUTOINCREMENT,
            sup_code TEXT UNIQUE NOT NULL,
            sup_type TEXT,
            first_name TEXT,
            last_name TEXT,
            company_name TEXT,
            country TEXT,
            city TEXT,
            phone TEXT,
            email TEXT,
            date_of_birth DATE,
            nif INT,
            created_at TEXT,
            updated_at TEXT
        );
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS clients(
            cli_id INTEGER PRIMARY KEY AUTOINCREMENT,
            cli_code TEXT UNIQUE NOT NULL,
            cli_type TEXT,
            first_name TEXT,
            last_name TEXT,
            company_name TEXT,
            country TEXT,
            city TEXT,
            phone TEXT,
            email TEXT,
            date_of_birth DATE,
            nif INT,
            created_at TEXT,
            updated_at TEXT
        );
        """
    )

    # quantity IS CALCULATED
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS materials(
            mat_id INTEGER PRIMARY KEY AUTOINCREMENT,
            mat_code TEXT UNIQUE NOT NULL,
            name TEXT,
            category TEXT,
            quantity INTEGER NOT NULL DEFAULT 0,
            base_unit TEXT,
            unit_price FLOAT NOT NULL DEFAULT 0,
            status TEXT NOT NULL DEFAULT "active",
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
            pro_id INTEGER PRIMARY KEY AUTOINCREMENT,
            pro_code TEXT UNIQUE NOT NULL,
            name TEXT,
            category TEXT,
            quantity INTEGER NOT NULL DEFAULT 0,
            base_unit TEXT,
            unit_price FLOAT NOT NULL DEFAULT 0,
            production_cost FLOAT,
            created_at TEXT,
            updated_at TEXT
        );
        """
    )

    # total_price IS CALCULATED
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS movements_in(
            mov_nr INTEGER PRIMARY KEY AUTOINCREMENT,
            mat_id TEXT,
            sup_id TEXT,
            quantity INTEGER NOT NULL DEFAULT 0,
            total_price FLOAT,
            created_at TEXT,
            updated_at TEXT,
            FOREIGN KEY(mat_id) REFERENCES materials(mat_id),
            FOREIGN KEY(sup_id) REFERENCES supliers(sup_id)
        );
        """
    )

    # total_price IS CALCULATED
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS movements_out(
            mov_nr INTEGER PRIMARY KEY AUTOINCREMENT,
            pro_id TEXT,
            cli_id TEXT,
            quantity INTEGER NOT NULL DEFAULT 0,
            total_price FLOAT,
            created_at TEXT,
            updated_at TEXT,
            FOREIGN KEY(pro_id) REFERENCES materials(pro_id),
            FOREIGN KEY(cli_id) REFERENCES supliers(cli_id)
        );
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS product_materials(
            pro_id TEXT,
            mat_id TEXT,
            quantity INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY(pro_id) REFERENCES materials(pro_id),
            FOREIGN KEY(mat_id) REFERENCES supliers(mat_id)
        );
        """
    )

    # total_cost IS CALCULATED
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS production_line(
            prdc_nr INTEGER PRIMARY KEY AUTOINCREMENT,
            pro_id TEXT,
            quantity INTEGER NOT NULL DEFAULT 0,
            total_cost FLOAT,
            created_at TEXT,
            updated_at TEXT,
            FOREIGN KEY(pro_id) REFERENCES materials(pro_id)
        );
        """
    )

    connection.commit()
    connection.close()
