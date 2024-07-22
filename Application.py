from LoginWindow import LoginWindow
from MainWindow import MainWindow


class Application:

    def __init__(self):
        self.__login_window = LoginWindow()
        self.__main_window = None

    def run(self):
        self.__login_window.display_window()
        self.__main_window = MainWindow(self.__login_window.get_connection(), self.__login_window.get_database())
        self.__main_window.display_window()
