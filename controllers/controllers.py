#! /usr/bin/env python3
# coding: utf-8
from views import views
from models import models

class Controller:

    def __init__(self):
        self.model = models.Players
        self.view = views.HomePage()

    def start(self):
        self.start = True
        while self.start:
            self.view.show_menu()
            self.view.ask_user_choice()

    def quit(self):
        self.start = False


if __name__ == "__main__":
    pass

