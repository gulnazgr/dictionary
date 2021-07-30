import json
import sqlite3
from jsonschema import validate

DEFAULT_DB_PATH = "./shop.db"


def create_goods_table(db_con: sqlite3.Connection) -> None:
    """Создает таблицу goods, если ещё она не создана."""
    sql = """
        CREATE TABLE IF NOT EXISTS goods (
            id INTEGER PRIMARY KEY AUTOINCREMENT, -- 'уникальный идентификатор товара'
            name VARCHAR NOT NULL, -- 'наименование товара'
            package_height FLOAT NOT NULL, -- 'высота упакованного товара'
            package_width FLOAT NOT NULL -- 'ширина упакованного товара
        );
    """

    db_con.execute(sql)
    db_con.commit()


def create_shops_goods_table(db_con: sqlite3.Connection) -> None:
    """Создает таблицу shops_goods, если ещё она не создана."""
    sql = """
        CREATE TABLE IF NOT EXISTS shops_goods (
            id INTEGER PRIMARY KEY AUTOINCREMENT, -- 'идентификатор записи'
            id_good INTEGER NOT NULL, -- 'идентификатор товара'
            location VARCHAR NOT NULL UNIQUE, -- 'адрес магазина'
            amount INTEGER NOT NULL, -- 'количество этого товара в этом магазине'
            FOREIGN KEY (id_good) REFERENCES goods (id)
        );
    """

    db_con.execute(sql)
    db_con.commit()


def inventory(good: dict, db_path: str = DEFAULT_DB_PATH) -> None:
    """Учёт товаров. Принемает json и путь к базе данных."""
    # загружаем json-схему
    with open("./goods.schema.json", "r", encoding="utf-8") as f:
        schema = json.load(f)

    # валидируем данные
    validate(good, schema)

    # подключаемся к базе данных
    with sqlite3.connect(db_path) as db_con:
        # создаем таблицы
        create_goods_table(db_con)
        create_shops_goods_table(db_con)

        good_id = good["id"]
        good_name = good["name"]
        package_params = good["package_params"]
        good_height = package_params["height"]
        good_width = package_params["width"]

        exist_good = db_con.execute("SELECT * FROM goods WHERE id = ? LIMIT 1", (good_id,)).fetchone()

        if exist_good:
            db_con.execute(
                "UPDATE goods SET name = ?, package_height = ?, package_width = ? WHERE id = ?",
                (good_name, good_height, good_width, good_id),
            )

            for item in good["location_and_quantity"]:
                location = item["location"]
                amount = item["amount"]

                exist_shop = db_con.execute(
                    "SELECT * FROM shops_goods WHERE id_good = ? AND location = ?", (good_id, location)
                ).fetchone()

                if exist_shop:
                    db_con.execute(
                        "UPDATE shops_goods SET amount = ? WHERE id_good = ? AND location = ?",
                        (amount, good_id, location),
                    )
                else:
                    db_con.execute(
                        "INSERT INTO shops_goods (id_good, location, amount) VALUES (?, ?, ?);",
                        (good_id, location, amount),
                    )
        else:
            db_con.execute(
                "INSERT INTO goods (id, name, package_height, package_width) VALUES (?, ?, ?, ?);",
                (good_id, good_name, good_height, good_width),
            )

            for item in good["location_and_quantity"]:
                location = item["location"]
                amount = item["amount"]

                db_con.execute(
                    "INSERT INTO shops_goods (id_good, location, amount) VALUES (?, ?, ?);", (good_id, location, amount)
                )

        db_con.commit()
