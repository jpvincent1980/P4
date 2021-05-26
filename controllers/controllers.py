#! /usr/bin/env python3
# coding: utf-8
from views import views
from models import models
import os

class Controller:

    def __init__(self):
        self.model = models.Players
        self.view = views.HomePage()

    def start(self):
        self.start = True
        compteur = 0
        while self.start:
            if compteur == 0:
                self.view.show_title()
            compteur += 1
            self.view.show_menu()
            new_view = self.view.ask_user_choice()
            self.view = new_view

if __name__ == "__main__":
    pass
