import unittest
from src.Delivery import calculate_delivery_cost

class TestDeliveryService(unittest.TestCase):

    # границы веса и расстояния
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

    # тип упаковки несуществующий
    def test_invalid_package_type_returns_error(self):
        cost, date = calculate_delivery_cost(2.0, 100, "неизвестный_тип")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    # расчёты стандартной доставки
    def test_standard_delivery_calculation(self):
        cost, date = calculate_delivery_cost(2.0, 100, "обычный", is_express=False)
        self.assertEqual(cost, 700)
        self.assertEqual(date, "2026-09-04")

    def test_heavy_package_weight_category_2(self):
        cost, _ = calculate_delivery_cost(10.0, 100, "обычный", is_express=False)
        self.assertEqual(cost, 840)

    def test_super_heavy_package_weight_category_3(self):
        cost, _ = calculate_delivery_cost(25.0, 100, "обычный", is_express=False)
        self.assertEqual(cost, 1050)

    # надбавки
    def test_fragile_package_surcharge(self):
        cost, _ = calculate_delivery_cost(2.0, 100, "хрупкий", is_express=False)
        self.assertEqual(cost, 1000)

    def test_hazardous_package_surcharge(self):
        cost, _ = calculate_delivery_cost(2.0, 100, "опасный", is_express=False)
        self.assertEqual(cost, 1700)

    # экспресс
    def test_express_delivery_surcharge(self):
        cost, _ = calculate_delivery_cost(2.0, 100, "обычный", is_express=True)
        self.assertEqual(cost, 1050)

    def test_express_delivery_time_minimum_one_day(self):
        _, date = calculate_delivery_cost(2.0, 100, "обычный", is_express=True)
        self.assertEqual(date, "2026-09-04")


if __name__ == "__main__":
    unittest.main()