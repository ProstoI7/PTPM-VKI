import logging
class Controller:

    def __init__(self, calculator, database, user_io, external_service):
        self.calculator = calculator
        self.database = database
        self.user_io = user_io
        self.external_service = external_service

    def run(self):
        a_str = self.user_io.get_input("Введите сторону a: ")
        b_str = self.user_io.get_input("Введите сторону b: ")
        c_str = self.user_io.get_input("Введите сторону c: ")

        try:
            a = float(a_str)
            b = float(b_str)
            c = float(c_str)
            db_key_valid = True
        except ValueError:
            db_key_valid = False

        if db_key_valid:
            record = self.database.get_record(a, b, c)
            if record:
                triangle_type = record["triangle_type"]
                error_message = record["error_message"]
                result_message = (
                    f"Из БД: тип={triangle_type}"
                    + (f", ошибка={error_message}" if error_message else "")
                )
            else:
                triangle_type, error_message, coordinates = self.calculator.process_triangle(
                    a_str, b_str, c_str
                )
                self.database.add_record(a, b, c, triangle_type, error_message)
                result_message = (
                    f"Вычислено: тип={triangle_type}, вершины={coordinates}"
                    + (f", ошибка={error_message}" if error_message else "")
                )
        else:
            triangle_type, error_message, coordinates = self.calculator.process_triangle(
                a_str, b_str, c_str
            )
            result_message = (
                f"Вычислено: тип={triangle_type}, вершины={coordinates}"
                + (f", ошибка={error_message}" if error_message else "")
            )

        self.external_service.send_result(result_message)
        self.user_io.show_output(result_message)
        return result_message