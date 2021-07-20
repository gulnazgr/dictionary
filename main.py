import sqlite3
#создаем и соединяем бд
con = sqlite3.connect('shop.db')
#обеспечивает закрытия соединения в случае ошибки
with con:
    cur = con.cursor()
#создаем таблицы
    cur.execute("""CREATE TABLE IF NOT EXISTS goods(
       id INT PRIMARY KEY NOT NULL,
       name VARCHAR NOT NULL,
       package_height FLOAT NOT NULL,
       package_width FLOAT NOT NULL
       );
    """)
    con.commit()

    cur.execute("""CREATE TABLE IF NOT EXISTS shops_goods(
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       id_good INT NOT NULL,
       location VARCHAR NOT NULL,
        amount INT NOT NULL 
          
       );
    """)
    con.commit()
    #добавление данных
    cur.execute("""INSERT INTO goods(id, name, package_height, package_width) 
       VALUES('123', 'Телевизор', '5', '10');""")
    con.commit()

    cur.execute("""INSERT INTO shops_goods( id_good, location, amount) 
       VALUES('123', 'Магазин на Ленина', '7');""")
    con.commit()

con.close()