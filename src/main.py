import logging
import os
import sys

from calculations import TriangleCalculator
from database import TriangleDatabase
from user_io import ConsoleUserIO
from external_service import EmailServiceStub
from controller import Controller

def main():
    os.makedirs("Logs", exist_ok=True)
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s | [%(levelname)-7s] | %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("Logs/file_txt.log", encoding="utf-8"),
        ],
    )

    db = TriangleDatabase("triangles.db")

    controller = Controller(
        calculator=TriangleCalculator(),
        database=db,
        user_io=ConsoleUserIO(),
        external_service=EmailServiceStub(),
    )
    controller.run()
    db.close()

if __name__ == "__main__":
    main()