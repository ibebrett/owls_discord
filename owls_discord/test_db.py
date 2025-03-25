import pytest
from .db import DB


@pytest.fixture
def test_db(tmp_path) -> DB:
    db_path = tmp_path / "db"
    db = DB(db_path)
    db.setup()

    return db


def test_toppings(test_db):
    test_db.get_toppings() == []

    test_db.add_topping("pineapple")

    assert test_db.get_toppings() == ["pineapple"]


def test_interaction(test_db):
    test_db.add_interaction(10, "chat")
    test_db.add_interaction(100, "pizza")

    assert set(test_db.get_interactions()) == {(10, "chat"), (100, "pizza")}
