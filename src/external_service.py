from abc import ABC, abstractmethod

class ExternalService(ABC):

    @abstractmethod
    def send_result(self, result: str) -> bool:
        ...

class EmailServiceStub(ExternalService):

    def __init__(self):
        self.sent_messages = []

    def send_result(self, result: str) -> bool:
        # Имитация
        self.sent_messages.append(result)
        return True