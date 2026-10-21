from abc import ABC, abstractmethod

class UserIO(ABC):

    @abstractmethod
    def get_input(self, prompt: str) -> str:
        ...

    @abstractmethod
    def show_output(self, message: str) -> None:
        ...

class ConsoleUserIO(UserIO):

    def get_input(self, prompt: str) -> str:
        return input(prompt)

    def show_output(self, message: str) -> None:
        print(message)