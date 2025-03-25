from typing import List, Iterable, Tuple

import os
import sqlite3

db_path = os.path.join(os.path.dirname(__file__), "db")


class DB:
    def __init__(self, db_path=db_path):
        self.conn = sqlite3.connect(db_path)

    def setup(self):
        cur = self.conn.cursor()
        cur.execute("CREATE TABLE toppings(name VARCHAR)")
        cur.execute("CREATE TABLE interaction(time INT, style VARCHAR)")
        self.conn.commit()

    def get_toppings(self) -> List[str]:
        curr = self.conn.execute("select name from toppings")
        results = []
        for (name,) in curr.fetchall():
            results.append(name)

        return results

    def add_topping(self, name: str):
        self.conn.execute("insert into toppings values (?)", (name,))
        self.conn.commit()

    def add_interaction(self, time: int, style: str) -> None:
        self.conn.execute("insert into interaction values (?, ?)", (time, style))
        self.conn.commit()

    def get_interactions(self) -> Iterable[Tuple[int, str]]:
        self.conn.commit()
        curr = self.conn.execute("select time, style from interaction")
        yield from curr.fetchall()


def setup_db():
    db = DB()
    db.setup()
