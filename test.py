import unittest
import json
import sqlite3
from main import inventory, create_goods_table, create_shops_goods_table


def load_json(path: str) -> dict:
    """Загружает данные из json-файла."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data


class TestGoodUpdate(unittest.TestCase):
    """Проверяет обновление товара."""

    def setUp(self) -> None:
        """Настраиваем проверяемую систему перед каждым тестом."""
        good_id = 123
        good_name = "Телевизор"
        good_height = 5
        good_width = 10
        location_and_quantity = [
            {"location": "Магазин на Ленина", "amount": 7},
            {"location": "Магазин в центре", "amount": 3},
        ]

        db_con = sqlite3.connect("./test.db")

        db_con.execute("DROP TABLE IF EXISTS goods;")
        db_con.execute("DROP TABLE IF EXISTS shops_goods;")

        create_goods_table(db_con)
        create_shops_goods_table(db_con)

        db_con.execute(
            "INSERT INTO goods (id, name, package_height, package_width) VALUES (?, ?, ?, ?);",
            (good_id, good_name, good_height, good_width),
        )

        for item in location_and_quantity:
            location = item["location"]
            amount = item["amount"]

            db_con.execute(
                "INSERT INTO shops_goods (id_good, location, amount) VALUES (?, ?, ?);",
                (good_id, location, amount),
            )

    def tearDown(self) -> None:
        """Подчищаем данные после каждого теста."""
        db_con = sqlite3.connect("./test.db")
        db_con.execute("DROP TABLE IF EXISTS goods;")
        db_con.execute("DROP TABLE IF EXISTS shops_goods;")

    def test_update(self) -> None:
        """Проверяет обновление товара."""
        test_name = "Телевизор LG"
        test_amount = 7

        test_good = {
            "id": 123,
            "name": test_name,
            "package_params": {"width": 10, "height": 5},
            "location_and_quantity": [{"location": "Магазин в центре", "amount": test_amount}],
        }

        inventory(test_good, "./test.db")

        db_con = sqlite3.connect("./test.db")

        row = db_con.execute("SELECT * FROM goods WHERE id = 123 LIMIT 1").fetchone()

        name = row[1]

        self.assertEqual(test_name, name)

        row = db_con.execute(
            "SELECT * FROM shops_goods WHERE id_good = 123 AND location = 'Магазин в центре'"
        ).fetchone()

        amount = row[3]

        self.assertEqual(test_amount, amount)


if __name__ == "__main__":
    unittest.main()
