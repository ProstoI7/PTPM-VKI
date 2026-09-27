import unittest
from src.Delivery import calculate_delivery_cost


class TestDeliveryService(unittest.TestCase):

    # 1. Проверки граничных значений веса и расстояния
    def test_weight_below_min_returns_error(self):
        cost, date = calculate_delivery_cost(0.05, 100, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_weight_above_max_returns_error(self):
        cost, date = calculate_delivery_cost(50.1, 100, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_distance_below_min_returns_error(self):
        cost, date = calculate_delivery_cost(2.0, 0, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_distance_above_max_returns_error(self):
        cost, date = calculate_delivery_cost(2.0, 5001, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    # 2. Проверка типов упаковки
    def test_invalid_package_type_returns_error(self):
        cost, date = calculate_delivery_cost(2.0, 100, "неизвестный_тип")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    # 3. Базовый расчет стандартной доставки
    def test_standard_delivery_calculation(self):
        # Weight=2.0 (<5.0, coef=1.0), distance=100 (cost = 200 + 100*5 = 700)
        # Days needed = max(1, 100//500) = 1 day -> 2026-09-04
        cost, date = calculate_delivery_cost(2.0, 100, "обычный", is_express=False)
        self.assertEqual(cost, 700)
        self.assertEqual(date, "2026-09-04")

    def test_heavy_package_weight_category_2(self):
        # Weight=10.0 (5..20, coef=1.2), distance=100 (base = 700 -> 700 * 1.2 = 840)
        cost, _ = calculate_delivery_cost(10.0, 100, "обычный", is_express=False)
        self.assertEqual(cost, 840)

    def test_super_heavy_package_weight_category_3(self):
        # Weight=25.0 (>=20, coef=1.5), distance=100 (base = 700 -> 700 * 1.5 = 1050)
        cost, _ = calculate_delivery_cost(25.0, 100, "обычный", is_express=False)
        self.assertEqual(cost, 1050)

    # 4. Проверка надбавок за тип груза
    def test_fragile_package_surcharge(self):
        # Base=700 + 300 = 1000
        cost, _ = calculate_delivery_cost(2.0, 100, "хрупкий", is_express=False)
        self.assertEqual(cost, 1000)

    def test_hazardous_package_surcharge(self):
        # Base=700 + 1000 = 1700
        cost, _ = calculate_delivery_cost(2.0, 100, "опасный", is_express=False)
        self.assertEqual(cost, 1700)

    # 5. Экспресс-доставка (Тесты для обнаружения багов в исходном коде)
    def test_express_delivery_surcharge(self):
        # Base=700. Ожидается: 700 * 1.5 = 1050. В исходном коде: 700 * 0.5 = 350.
        cost, _ = calculate_delivery_cost(2.0, 100, "обычный", is_express=True)
        self.assertEqual(cost, 1050)

    def test_express_delivery_time_minimum_one_day(self):
        # Distance=100 -> days_needed = 1. В исходном коде 1 // 2 = 0 дней -> дата 2026-09-03.
        # Должна оставаться минимум 1 день -> дата 2026-09-04.
        _, date = calculate_delivery_cost(2.0, 100, "обычный", is_express=True)
        self.assertEqual(date, "2026-09-04")


if __name__ == "__main__":
    unittest.main()