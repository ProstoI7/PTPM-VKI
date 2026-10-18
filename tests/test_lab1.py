import unittest
from src.lab1 import process_triangle


class TestMyProject(unittest.TestCase):

    # 1. Валидные сценарии (Корректное определение типов)
    def test_equilateral_triangle_returns_correct_type(self):
        triangle_type, _ = process_triangle("10", "10", "10")
        self.assertEqual(triangle_type, "равносторонний")

    def test_isosceles_triangle_returns_correct_type(self):
        triangle_type, _ = process_triangle("10", "10", "12")
        self.assertEqual(triangle_type, "равнобедренный")

    def test_scalene_triangle_returns_correct_type(self):
        triangle_type, _ = process_triangle("3", "4", "5")
        self.assertEqual(triangle_type, "разносторонний")

    def test_float_strings_return_correct_type(self):
        triangle_type, _ = process_triangle("5.5", "5.5", "8.2")
        self.assertEqual(triangle_type, "равнобедренный")

    # 2. Невалидный ввод (ValueError)
    def test_invalid_string_input_a_returns_error_code(self):
        type_res, coords = process_triangle("abc", "10", "10")
        self.assertEqual(type_res, "")
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])

    def test_invalid_string_input_b_returns_error_code(self):
        type_res, coords = process_triangle("10", "xyz", "10")
        self.assertEqual(type_res, "")
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])

    def test_invalid_string_input_c_returns_error_code(self):
        type_res, coords = process_triangle("10", "10", "???")
        self.assertEqual(type_res, "")
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])

    # 3. Граничные и невалидные длины сторон (<= 0)
    def test_zero_side_a_returns_not_triangle(self):
        type_res, coords = process_triangle("0", "5", "5")
        self.assertEqual(type_res, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

    def test_negative_side_a_returns_not_triangle(self):
        type_res, coords = process_triangle("-3", "4", "5")
        self.assertEqual(type_res, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

    def test_negative_side_b_returns_not_triangle(self):
        type_res, coords = process_triangle("3", "-4", "5")
        self.assertEqual(type_res, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

    def test_negative_side_c_returns_not_triangle(self):
        type_res, coords = process_triangle("3", "4", "-5")
        self.assertEqual(type_res, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

    # 4. Нарушение неравенства треугольника (a + b <= c)
    def test_sum_of_two_sides_equal_third_returns_not_triangle(self):
        type_res, coords = process_triangle("2", "3", "5")
        self.assertEqual(type_res, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

    def test_sum_of_two_sides_less_than_third_returns_not_triangle(self):
        type_res, coords = process_triangle("10", "10", "100")
        self.assertEqual(type_res, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

    def test_triangle_inequality_permutation_1(self):
        type_res, _ = process_triangle("100", "10", "10")
        self.assertEqual(type_res, "не треугольник")

    def test_triangle_inequality_permutation_2(self):
        type_res, _ = process_triangle("10", "100", "10")
        self.assertEqual(type_res, "не треугольник")

    # 5. Проверка геометрии и масштабирования координат
    def test_equilateral_coordinates_bounds(self):
        _, coords = process_triangle("50", "50", "50")
        for x, y in coords:
            self.assertTrue(0 <= x <= 100)
            self.assertTrue(0 <= y <= 100)

    def test_large_equilateral_coordinates_bounds(self):
        _, coords = process_triangle("200", "200", "200")
        for x, y in coords:
            self.assertTrue(0 <= x <= 100)
            self.assertTrue(0 <= y <= 100)

    def test_right_triangle_coordinates_bounds(self):
        _, coords = process_triangle("3", "4", "5")
        for x, y in coords:
            self.assertTrue(0 <= x <= 100)
            self.assertTrue(0 <= y <= 100)

    def test_isosceles_equal_sides_permutation(self):
        t1, _ = process_triangle("5", "5", "8")
        t2, _ = process_triangle("5", "8", "5")
        t3, _ = process_triangle("8", "5", "5")
        self.assertEqual(t1, "равнобедренный")
        self.assertEqual(t2, "равнобедренный")
        self.assertEqual(t3, "равнобедренный")

    def test_very_small_valid_triangle(self):
        type_res, coords = process_triangle("0.1", "0.1", "0.1")
        self.assertEqual(type_res, "равносторонний")
        self.assertEqual(len(coords), 3)

    def test_returns_tuple_structure(self):
        res = process_triangle("3", "4", "5")
        self.assertIsInstance(res, tuple)
        self.assertEqual(len(res), 2)


if __name__ == "__main__":
    unittest.main()