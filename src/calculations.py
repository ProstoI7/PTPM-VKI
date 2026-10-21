import math
import logging

class TriangleCalculator:
    def process_triangle(self, side_a_str: str, side_b_str: str, side_c_str: str):
        logging.info(f"Старт обработки сторон: a='{side_a_str}', b='{side_b_str}', c='{side_c_str}'")

        try:
            a = float(side_a_str)
            b = float(side_b_str)
            c = float(side_c_str)
        except ValueError:
            logging.error("Входные данные не являются действительными числами.")
            return "не треугольник", "Входные данные не являются действительными числами", [(-2, -2), (-2, -2), (-2, -2)]

        if a <= 0 or b <= 0 or c <= 0:
            logging.error(f"Недопустимые стороны: ({a}, {b}, {c})")
            return "не треугольник", "Длины сторон должны быть > 0", [(-1, -1), (-1, -1), (-1, -1)]

        if (a + b <= c) or (a + c <= b) or (b + c <= a):
            logging.warning(f"Фигура не существует: ({a}, {b}, {c}).")
            return "не треугольник", "Одна из сторон больше или равна сумме двух других", [(-1, -1), (-1, -1), (-1, -1)]

        if math.isclose(a, b) and math.isclose(b, c):
            triangle_type = "равносторонний"
        elif math.isclose(a, b) or math.isclose(b, c) or math.isclose(a, c):
            triangle_type = "равнобедренный"
        else:
            triangle_type = "разносторонний"

        try:
            cos_alpha = (a ** 2 + c ** 2 - b ** 2) / (2 * a * c)
            cos_alpha = max(-1.0, min(1.0, cos_alpha))
            alpha = math.acos(cos_alpha)

            cx = c * math.cos(alpha)
            cy = c * math.sin(alpha)

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
        except Exception:
            logging.error("Сбой вычислений при расчете координат.")
            return "не треугольник", "Сбой вычислений координат", [(-1, -1), (-1, -1), (-1, -1)]

        logging.info(f"Результат: тип='{triangle_type}', вершины={coordinates}")
        return triangle_type, None, coordinates