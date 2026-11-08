"""Тесты для модуля parser (Модуль 2)."""

import sqlite3
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.database import DatabaseRepository
from src.parser import ForumParser


FIXTURE_PATH = Path(__file__).resolve().parent / "fixtures" / "sample_page.html"


class TestForumParser(unittest.TestCase):
    """Тесты парсинга HTML-фикстуры и сохранения в БД."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.html = FIXTURE_PATH.read_text(encoding="utf-8")

    def setUp(self) -> None:
        self.parser = ForumParser()

    # ----------------------- parse_html ----------------------------- #
    def test_parse_html_extracts_all_valid_comments(self) -> None:
        result = self.parser.parse_html(self.html)
        self.assertEqual(len(result), 3)
        self.assertEqual([r["id"] for r in result], [101, 102, 103])

    def test_parse_html_extracts_fields_correctly(self) -> None:
        result = self.parser.parse_html(self.html)
        first = result[0]
        self.assertEqual(first["id"], 101)
        self.assertEqual(first["name"], "alice")
        self.assertIn("<b>первое</b>", first["message"])

    def test_parse_html_skips_missing_and_invalid_id(self) -> None:
        result = self.parser.parse_html(self.html)
        names = [r["name"] for r in result]
        self.assertNotIn("ghost", names)       # без ID
        self.assertNotIn("charlie", names)     # невалидный ID

    # ---------------------- save_to_db ------------------------------ #
    def test_save_to_db_persists_data(self) -> None:
        repo = DatabaseRepository(":memory:")
        try:
            parsed = self.parser.parse_html(self.html)
            saved = self.parser.save_to_db(parsed, repo)
            self.assertEqual(saved, 3)

            row = repo.get_by_id(101)
            self.assertIsNotNone(row)
            self.assertEqual(row["name"], "alice")

            alice_rows = repo.get_by_name("alice")
            self.assertEqual(len(alice_rows), 2)
        finally:
            repo.close()

    def test_save_to_db_skips_duplicates(self) -> None:
        repo = DatabaseRepository(":memory:")
        try:
            parsed = self.parser.parse_html(self.html)
            self.parser.save_to_db(parsed, repo)
            # повторное сохранение — дубликаты должны быть пропущены
            saved_again = self.parser.save_to_db(parsed, repo)
            self.assertEqual(saved_again, 0)
        finally:
            repo.close()


if __name__ == "__main__":
    unittest.main()