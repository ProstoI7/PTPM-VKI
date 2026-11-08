"""
Модуль 1: Библиотека классов для работы с базой данных (SQLite).

Класс DatabaseRepository предоставляет CRUD-интерфейс над таблицей comments.
"""

from __future__ import annotations

import sqlite3
from typing import Optional


# Максимальные длины полей (из ТЗ)
MAX_NAME_LEN = 256
MAX_MESSAGE_LEN = 8096


class DatabaseRepository:
    """Репозиторий для работы с таблицей comments в SQLite."""

    def __init__(self, db_path: str = ":memory:") -> None:
        """
        Инициализация репозитория.

        :param db_path: путь к файлу БД или ':memory:' для тестов.
        """
        self.db_path = db_path
        self._connection = sqlite3.connect(db_path)
        self._connection.row_factory = sqlite3.Row
        self._create_table()

    # ------------------------------------------------------------------ #
    #                         Внутренние методы                          #
    # ------------------------------------------------------------------ #
    def _create_table(self) -> None:
        """Создаёт таблицу comments, если её ещё нет."""
        with self._connection:
            self._connection.execute(
                """
                CREATE TABLE IF NOT EXISTS comments (
                    id      INTEGER PRIMARY KEY,
                    name    TEXT NOT NULL CHECK (length(name) <= 256),
                    message TEXT NOT NULL CHECK (length(message) <= 8096)
                )
                """
            )

    @staticmethod
    def _validate_id(comment_id: int) -> None:
        if not isinstance(comment_id, int) or isinstance(comment_id, bool):
            raise TypeError("comment_id должен быть целым числом (int).")

    @staticmethod
    def _validate_name(username: str) -> None:
        if not isinstance(username, str):
            raise TypeError("username должен быть строкой (str).")
        if not username:
            raise ValueError("username не может быть пустым.")
        if len(username) > MAX_NAME_LEN:
            raise ValueError(
                f"Длина username превышает {MAX_NAME_LEN} символов."
            )

    @staticmethod
    def _validate_message(message: str) -> None:
        if not isinstance(message, str):
            raise TypeError("message должен быть строкой (str).")
        if len(message) > MAX_MESSAGE_LEN:
            raise ValueError(
                f"Длина message превышает {MAX_MESSAGE_LEN} символов."
            )

    # ------------------------------------------------------------------ #
    #                         Публичный API                              #
    # ------------------------------------------------------------------ #
    def get_by_id(self, comment_id: int) -> Optional[dict]:
        """Возвращает запись по ID или None, если её нет."""
        self._validate_id(comment_id)
        cursor = self._connection.execute(
            "SELECT id, name, message FROM comments WHERE id = ?",
            (comment_id,),
        )
        row = cursor.fetchone()
        return dict(row) if row else None

    def get_by_name(self, username: str) -> list[dict]:
        """Возвращает все записи пользователя с указанным именем."""
        self._validate_name(username)
        cursor = self._connection.execute(
            "SELECT id, name, message FROM comments WHERE name = ? ORDER BY id",
            (username,),
        )
        return [dict(row) for row in cursor.fetchall()]

    def add(self, comment_id: int, username: str, message: str) -> bool:
        """
        Добавляет новую запись.

        :raises TypeError: неверный тип данных.
        :raises ValueError: превышена длина строк.
        :raises sqlite3.IntegrityError: дублирование ID.
        :return: True при успехе.
        """
        self._validate_id(comment_id)
        self._validate_name(username)
        self._validate_message(message)

        with self._connection:
            self._connection.execute(
                "INSERT INTO comments (id, name, message) VALUES (?, ?, ?)",
                (comment_id, username, message),
            )
        return True

    def update(self, comment_id: int, new_message: str) -> bool:
        """
        Обновляет поле message у записи с заданным ID.

        :raises TypeError: неверный тип.
        :raises ValueError: превышена длина строки.
        :raises LookupError: запись с таким ID не найдена.
        :return: True при успехе.
        """
        self._validate_id(comment_id)
        self._validate_message(new_message)

        with self._connection:
            cursor = self._connection.execute(
                "UPDATE comments SET message = ? WHERE id = ?",
                (new_message, comment_id),
            )
        if cursor.rowcount == 0:
            raise LookupError(f"Запись с id={comment_id} не найдена.")
        return True

    def delete(self, comment_id: int) -> bool:
        """
        Удаляет запись по ID.

        :raises LookupError: запись не найдена.
        :return: True при успехе.
        """
        self._validate_id(comment_id)
        with self._connection:
            cursor = self._connection.execute(
                "DELETE FROM comments WHERE id = ?", (comment_id,)
            )
        if cursor.rowcount == 0:
            raise LookupError(f"Запись с id={comment_id} не найдена.")
        return True

    # ------------------------------------------------------------------ #
    #                         Утилиты                                    #
    # ------------------------------------------------------------------ #
    def close(self) -> None:
        """Закрывает соединение с БД."""
        self._connection.close()

    def __enter__(self) -> "DatabaseRepository":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()