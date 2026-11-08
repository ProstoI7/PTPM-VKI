"""Тесты для модуля database (Модуль 1)."""

import sqlite3
import sys
import unittest
from pathlib import Path

# добавляем корень проекта в sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.database import DatabaseRepository, MAX_MESSAGE_LEN, MAX_NAME_LEN


class TestDatabaseRepository(unittest.TestCase):
    """Тесты CRUD-операций над таблицей comments."""

    def setUp(self) -> None:
        self.repo = DatabaseRepository(":memory:")

    def tearDown(self) -> None:
        self.repo.close()

    # ------------------------------ add ------------------------------ #
    def test_add_success(self) -> None:
        result = self.repo.add(1, "alice", "Hello, world!")
        self.assertTrue(result)
        row = self.repo.get_by_id(1)
        self.assertIsNotNone(row)
        self.assertEqual(row["name"], "alice")
        self.assertEqual(row["message"], "Hello, world!")

    def test_add_duplicate_id_raises(self) -> None:
        self.repo.add(1, "alice", "First")
        with self.assertRaises(sqlite3.IntegrityError):
            self.repo.add(1, "bob", "Second")

    def test_add_too_long_message_raises(self) -> None:
        with self.assertRaises(ValueError):
            self.repo.add(1, "alice", "x" * (MAX_MESSAGE_LEN + 1))

    def test_add_invalid_types_raises(self) -> None:
        with self.assertRaises(TypeError):
            self.repo.add("1", "alice", "msg")  # type: ignore[arg-type]

    # --------------------------- get_by_id --------------------------- #
    def test_get_by_id_existing(self) -> None:
        self.repo.add(42, "bob", "Hi!")
        row = self.repo.get_by_id(42)
        self.assertEqual(row, {"id": 42, "name": "bob", "message": "Hi!"})

    def test_get_by_id_missing_returns_none(self) -> None:
        self.assertIsNone(self.repo.get_by_id(999))

    # -------------------------- get_by_name -------------------------- #
    def test_get_by_name_returns_all_user_comments(self) -> None:
        self.repo.add(1, "alice", "First")
        self.repo.add(2, "bob", "B")
        self.repo.add(3, "alice", "Second")

        rows = self.repo.get_by_name("alice")
        self.assertEqual(len(rows), 2)
        self.assertEqual({r["message"] for r in rows}, {"First", "Second"})

    def test_get_by_name_empty_result(self) -> None:
        self.assertEqual(self.repo.get_by_name("nobody"), [])

    # ----------------------------- update ---------------------------- #
    def test_update_success(self) -> None:
        self.repo.add(1, "alice", "old")
        self.assertTrue(self.repo.update(1, "new"))
        self.assertEqual(self.repo.get_by_id(1)["message"], "new")

    def test_update_missing_id_raises(self) -> None:
        with self.assertRaises(LookupError):
            self.repo.update(999, "anything")

    def test_update_too_long_message_raises(self) -> None:
        self.repo.add(1, "alice", "ok")
        with self.assertRaises(ValueError):
            self.repo.update(1, "x" * (MAX_MESSAGE_LEN + 1))

    # ----------------------------- delete ---------------------------- #
    def test_delete_success(self) -> None:
        self.repo.add(1, "alice", "msg")
        self.assertTrue(self.repo.delete(1))
        self.assertIsNone(self.repo.get_by_id(1))

    def test_delete_missing_id_raises(self) -> None:
        with self.assertRaises(LookupError):
            self.repo.delete(999)


if __name__ == "__main__":
    unittest.main()