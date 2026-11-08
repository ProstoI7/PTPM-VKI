"""
Модуль 2: Веб-парсер (компонент сбора данных).

Класс ForumParser извлекает ID, имя автора и текст сообщения
со страниц форумов / структурированных веб-ресурсов.
"""

from __future__ import annotations

from typing import Any

import requests
from bs4 import BeautifulSoup

from src.database import DatabaseRepository


DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

# CSS-селекторы под «эталонную» разметку форума
COMMENT_SELECTOR = "div.comment"
ID_ATTR = "data-comment-id"
AUTHOR_SELECTOR = ".comment-author"
MESSAGE_SELECTOR = ".comment-message"


class ForumParser:
    """Парсер сообщений форума."""

    def __init__(self, headers: dict | None = None, timeout: int = 10) -> None:
        self.headers = headers or DEFAULT_HEADERS
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    # ------------------------------------------------------------------ #
    #                         Публичный API                              #
    # ------------------------------------------------------------------ #
    def fetch_html(self, url: str) -> str:
        """Скачивает HTML-код страницы по URL."""
        response = self.session.get(url, timeout=self.timeout)
        response.raise_for_status()
        return response.text

    def parse_html(self, html: str) -> list[dict[str, Any]]:
        """
        Разбирает HTML-строку и возвращает список комментариев.

        Каждый элемент: {'id': int, 'name': str, 'message': str}
        """
        soup = BeautifulSoup(html, "lxml")
        parsed: list[dict[str, Any]] = []

        for block in soup.select(COMMENT_SELECTOR):
            raw_id = block.get(ID_ATTR)
            if raw_id is None:
                continue
            try:
                comment_id = int(raw_id)
            except (TypeError, ValueError):
                continue

            author_tag = block.select_one(AUTHOR_SELECTOR)
            message_tag = block.select_one(MESSAGE_SELECTOR)
            if author_tag is None or message_tag is None:
                continue

            name = author_tag.get_text(strip=True)
            # сохраняем внутреннюю HTML-разметку сообщения
            message = message_tag.decode_contents().strip()

            parsed.append(
                {"id": comment_id, "name": name, "message": message}
            )
        return parsed

    def parse_page(self, url: str) -> list[dict[str, Any]]:
        """Скачивает страницу по URL и парсит её содержимое."""
        return self.parse_html(self.fetch_html(url))

    def save_to_db(
        self,
        parsed_data: list[dict[str, Any]],
        repository: DatabaseRepository,
    ) -> int:
        """
        Сохраняет разобранные комментарии в БД через DatabaseRepository.

        Дублирующиеся ID пропускаются (без исключения).
        :return: количество успешно сохранённых записей.
        """
        import sqlite3

        saved = 0
        for item in parsed_data:
            try:
                repository.add(item["id"], item["name"], item["message"])
                saved += 1
            except sqlite3.IntegrityError:
                # запись с таким ID уже есть — пропускаем
                continue
        return saved