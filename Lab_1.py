import logging
import math
import os
import sys

def process_triangle(a_str: str, b_str: str, c_str: str):
    logging.info(f"Старт обработки сторон: a='{a_str}', b='{b_str}', c='{c_str}'")

    # делаем флоат
    try:
        a = float(a_str)
        b = float(b_str)
        c = float(c_str)
    except ValueError:
        logging.error("Входные данные не являются действительными числами.")
        logging.exception("Исключение ValueError:")
        return "", [(-2, -2), (-2, -2), (-2, -2)]

    # проверяем что всё положительно
    if a <= 0 or b <= 0 or c <= 0:
        logging.error(f"Недопустимые стороны: длины должны быть > 0. Передано: ({a}, {b}, {c})")
        return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

    # смотрим существует ли вообще такой треугольник
    if (a + b <= c) or (a + c <= b) or (b + c <= a):
        logging.warning(f"Фигура не существует: одна из сторон больше или равна сумме двух других ({a}, {b}, {c}).")
        return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

    # определяем его вид
    if math.isclose(a, b) and math.isclose(b, c):
        triangle_type = "равносторонний"
    elif math.isclose(a, b) or math.isclose(b, c) or math.isclose(a, c):
        triangle_type = "равнобедренный"
    else:
        triangle_type = "разносторонний"

    logging.info(f"Тип фигуры успешно определён: {triangle_type}")

    # определяем корды вершин в поле 100 на 100
    try:
        cos_alpha = (a ** 2 + c ** 2 - b ** 2) / (2 * a * c)
        cos_alpha = max(-1.0, min(1.0, cos_alpha))
        logging.debug(f"Вычислен cos(alpha): {cos_alpha}")

        alpha = math.acos(cos_alpha)
        logging.debug(f"Угол alpha (в радианах): {alpha}")

        cx = c * math.cos(alpha)
        cy = c * math.sin(alpha)
        logging.debug(f"Немасштабированные координаты C: ({cx}, {cy})")

        min_x = min(0.0, a, cx)
        max_x = max(0.0, a, cx)
        min_y = 0.0
        max_y = cy

        w = max_x - min_x
        h = max_y - min_y

        max_size = max(w, h)
        scale = 100.0 / max_size if max_size > 0 else 1.0

        p1 = (int(round((0.0 - min_x) * scale)), int(round((0.0 - min_y) * scale)))
        p2 = (int(round((a - min_x) * scale)), int(round((0.0 - min_y) * scale)))
        p3 = (int(round((cx - min_x) * scale)), int(round((cy - min_y) * scale)))

        coordinates = [p1, p2, p3]
        logging.info(f"Рассчитаны итоговые координаты: {coordinates}")

    except Exception:
        logging.error("Сбой вычислений при расчете координат.")
        logging.exception("Детали ошибки:")
        return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

    logging.info(f"Результат: тип='{triangle_type}', вершины={coordinates}")
    return triangle_type, coordinates

def main():
    os.makedirs("Logs", exist_ok=True)

    log_format = "%(asctime)s | [%(levelname)-7s] | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    logging.basicConfig(
        level=logging.DEBUG,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("Logs/file_txt.log", encoding="utf-8")
        ]
    )

    logging.info("Логгер успешно сконфигурирован")
    logging.info("Приложение запущено")

    test1 = process_triangle("50", "50", "50")
    print(f"Тест 1: {test1}\n" + "=" * 50)

    test2 = process_triangle("200", "200", "200")
    print(f"Тест 2: {test2}\n" + "=" * 50)

    test3 = process_triangle("3", "4", "5")
    print(f"Тест 3: {test3}\n" + "=" * 50)

    test4 = process_triangle("-3", "4", "5")
    print(f"Тест 4: {test4}\n" + "=" * 50)

    test5 = process_triangle("10", "10", "100")
    print(f"Тест 5: {test5}\n" + "=" * 50)

    test6 = process_triangle("хз)", "50", "50")
    print(f"Тест 6: {test6}")

    logging.info("Тестирование завершено")

if __name__ == "__main__":
    main()