from contextlib import contextmanager
import sqlite3


class Base:
    def __init__(self, db_path) -> None:
        self.db_path = db_path
        self._create_schema()
        self._create_views()

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def _create_schema(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
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
                    tax_id TEXT,
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
                    tax_id TEXT,
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

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS products(
                    code TEXT PRIMARY KEY NOT NULL,
                    name TEXT,
                    category TEXT,
                    base_unit TEXT,
                    unit_price FLOAT NOT NULL DEFAULT 0,
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
                    FOREIGN KEY(pro_code) REFERENCES products(code),
                    FOREIGN KEY(mat_code) REFERENCES materials(code)
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

    def _create_views(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE VIEW IF NOT EXISTS product_details AS
                SELECT
                    p.*,
                    (
                        COALESCE((SELECT SUM(quantity) FROM production_line WHERE pro_code = p.code), 0) -
                        COALESCE((SELECT SUM(quantity) FROM movements_out WHERE pro_code = p.code), 0)
                    ) AS quantity,
                    (
                        SELECT COALESCE(SUM(pm.quantity * m.unit_price), 0)
                        FROM product_materials pm
                        JOIN materials m ON pm.mat_code = m.code
                        WHERE pm.pro_code = p.code
                    ) AS production_cost
                FROM products p;
                """
            )
