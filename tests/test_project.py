import unittest
from unittest.mock import patch, MagicMock
from src.calculations import TriangleCalculator
from src.database import TriangleDatabase
from src.user_io import UserIO
from src.external_service import ExternalService, EmailServiceStub
from src.controller import Controller

class FakeUserIO(UserIO):

    def __init__(self, inputs):
        self._inputs = iter(inputs)
        self.outputs = []

    def get_input(self, prompt: str) -> str:
        return next(self._inputs)

    def show_output(self, message: str) -> None:
        self.outputs.append(message)

# класс вычислений (валидация + тип)
class TestTriangleCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = TriangleCalculator()

    def test_equilateral(self):
        t, err, coords = self.calc.process_triangle("50", "50", "50")
        self.assertEqual(t, "равносторонний")
        self.assertIsNone(err)
        self.assertEqual(len(coords), 3)

    def test_invalid_triangle_inequality(self):
        t, err, coords = self.calc.process_triangle("10", "10", "100")
        self.assertEqual(t, "не треугольник")
        self.assertIsNotNone(err)

    def test_non_numeric_input(self):
        t, err, _ = self.calc.process_triangle("хз)", "50", "50")
        self.assertEqual(t, "не треугольник")
        self.assertIsNotNone(err)

# класс БД (add/get/delete)
class TestTriangleDatabase(unittest.TestCase):

    def setUp(self):
        self.db = TriangleDatabase(":memory:")

    def tearDown(self):
        self.db.close()

    def test_add_get_delete(self):
        self.db.add_record(3, 4, 5, "разносторонний")
        rec = self.db.get_record(3, 4, 5)
        self.assertIsNotNone(rec)
        self.assertEqual(rec["triangle_type"], "разносторонний")

        self.db.delete_record(3, 4, 5)
        self.assertIsNone(self.db.get_record(3, 4, 5))

    def test_get_missing(self):
        self.assertIsNone(self.db.get_record(1, 2, 3))

# Controller + Calculator + DB + ExternalService
# Сценарий: данных нет в БД → вычисление → запись в БД → отправка
class TestControllerIntegration_ComputeAndSave(unittest.TestCase):

    def setUp(self):
        self.db = TriangleDatabase(":memory:")
        self.fake_io = FakeUserIO(["3", "4", "5"])
        self.ext_service = MagicMock(spec=ExternalService)
        self.ext_service.send_result.return_value = True
        self.controller = Controller(
            calculator=TriangleCalculator(),
            database=self.db,
            user_io=self.fake_io,
            external_service=self.ext_service,
        )

    def tearDown(self):
        self.db.close()

    def test_compute_save_and_send(self):
        result = self.controller.run()

        # результат вычислен
        self.assertIn("разносторонний", result)

        # запись сохранена в БД
        rec = self.db.get_record(3.0, 4.0, 5.0)
        self.assertIsNotNone(rec)
        self.assertEqual(rec["triangle_type"], "разносторонний")

        # внешняя зависимость вызвана
        self.ext_service.send_result.assert_called_once()
        sent_arg = self.ext_service.send_result.call_args[0][0]
        self.assertIn("разносторонний", sent_arg)

        # вывод пользователю выполнен
        self.assertEqual(len(self.fake_io.outputs), 1)

# Controller + DB
# Сценарий: данных уже есть в БД → берём из БД, не вычисляем
class TestControllerIntegration_CacheHit(unittest.TestCase):

    def setUp(self):
        self.db = TriangleDatabase(":memory:")

        self.db.add_record(50.0, 50.0, 50.0, "равносторонний", None)

        self.fake_io = FakeUserIO(["50", "50", "50"])
        self.ext_service = MagicMock(spec=ExternalService)
        self.ext_service.send_result.return_value = True
        self.calculator = MagicMock(spec=TriangleCalculator)
        self.controller = Controller(
            calculator=self.calculator,
            database=self.db,
            user_io=self.fake_io,
            external_service=self.ext_service,
        )

    def tearDown(self):
        self.db.close()

    def test_read_from_db_not_recompute(self):
        result = self.controller.run()

        self.calculator.process_triangle.assert_not_called()

        self.assertIn("Из БД", result)
        self.assertIn("равносторонний", result)

        self.ext_service.send_result.assert_called_once()


# Controller + UserIO (patch input) + ExternalService (patch)
# сценарий с подменой пользовательского ввода и сторонней зависимости
class TestControllerIntegration_EndToEndWithPatching(unittest.TestCase):

    @patch("builtins.input", side_effect=["10", "10", "100"])
    def test_end_to_end_with_patched_input(self, mock_input):
        from src.user_io import ConsoleUserIO

        db = TriangleDatabase(":memory:")
        ext = MagicMock(spec=ExternalService)
        ext.send_result.return_value = True

        controller = Controller(
            calculator=TriangleCalculator(),
            database=db,
            user_io=ConsoleUserIO(),
            external_service=ext,
        )

        with patch("builtins.print") as mock_print:
            result = controller.run()

        self.assertIn("не треугольник", result)

        self.assertEqual(mock_input.call_count, 3)

        ext.send_result.assert_called_once()

        rec = db.get_record(10.0, 10.0, 100.0)
        self.assertIsNotNone(rec)
        self.assertEqual(rec["triangle_type"], "не треугольник")
        self.assertIsNotNone(rec["error_message"])

        mock_print.assert_called_once()
        db.close()


if __name__ == "__main__":
    unittest.main(verbosity=2)