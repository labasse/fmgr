class UserInterface:
    def error(msg: str) -> None:
        pass


class ConsoleUI(UserInterface):
    def error(msg: str) -> None:
        print(msg)
