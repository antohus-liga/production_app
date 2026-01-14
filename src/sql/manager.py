from PySide6.QtSql import QSqlDatabase, QSqlQuery
from sql.db_initializer import db_path, initialize_schema


def get_connection() -> None:
    initialize_schema()

    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(db_path)
    if not db.open():
        print("Could not open the database")
        exit()


def calculate_pro_quant():
    query = QSqlQuery()
    if not query.exec(
        """
        UPDATE products
        SET quantity =
            COALESCE(
                (SELECT SUM(pl.quantity)
                 FROM production_line pl
                 WHERE pl.pro_code = products.code),
                0
            )
            -
            COALESCE(
                (SELECT SUM(mo.quantity)
                 FROM movements_out mo
                 WHERE mo.pro_code = products.code),
                0
            );
    """
    ):
        raise Exception(query.lastError().text())


def calculate_mat_quant():
    query = QSqlQuery()
    if not query.exec(
        """
        UPDATE materials
        SET quantity =
            COALESCE(
                (SELECT SUM(mi.quantity)
                 FROM movements_in mi
                 WHERE mi.mat_code = materials.code),
                0
            )
            -
            COALESCE(
                (
                    SELECT SUM(pm.quantity * COALESCE(pl.total_produced,0))
                    FROM product_materials pm
                    LEFT JOIN (
                        SELECT pro_code, SUM(quantity) AS total_produced
                        FROM production_line
                        GROUP BY pro_code
                    ) pl ON pl.pro_code = pm.pro_code
                    WHERE pm.mat_code = materials.code
                ),
                0
            );
        """
    ):
        raise Exception(query.lastError().text())


def calculate_mov_in_price():
    query = QSqlQuery()
    if not query.exec(
        """
        UPDATE movements_in
        SET total_price = ROUND(
            COALESCE(
                (SELECT m.unit_price
                 FROM materials m
                 WHERE m.code = movements_in.mat_code),
                0
            )
            *
            COALESCE(quantity, 0),
            2
        );
        """
    ):
        raise Exception(query.lastError().text())


def calculate_mov_out_price():
    query = QSqlQuery()
    if not query.exec(
        """
        UPDATE movements_out
        SET total_price = ROUND(
            COALESCE(
                (SELECT p.unit_price
                 FROM products p
                 WHERE p.code = movements_out.pro_code),
                0
            )
            *
            COALESCE(quantity, 0),
            2
        );
        """
    ):
        raise Exception(query.lastError().text())


def calculate_pro_cost():
    query = QSqlQuery()
    if not query.exec(
        """
        UPDATE products
        SET production_cost = ROUND(
            COALESCE(
                (
                    SELECT SUM(pm.quantity * COALESCE(m.unit_price,0))
                    FROM product_materials pm
                    LEFT JOIN materials m ON m.code = pm.mat_code
                    WHERE pm.pro_code = products.code
                ),
                0
            ),
            2
        );
    """
    ):
        raise Exception(query.lastError().text())


def calculate_prod_line_cost():
    query = QSqlQuery()
    if not query.exec(
        """
        UPDATE production_line
        SET total_cost = ROUND(
            COALESCE(
                (SELECT p.production_cost
                 FROM products p
                 WHERE p.code = production_line.pro_code),
                0
            )
            *
            COALESCE(quantity, 0),
            2
        );
    """
    ):
        raise Exception(query.lastError().text())
