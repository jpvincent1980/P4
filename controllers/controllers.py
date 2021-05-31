#! /usr/bin/env python3
# coding: utf-8
from views import views
from models import models

class Controller:
    """
        A class that controls the main.py script.

        Attributes
        ----------
        model -> represents the Model of this MVC project
        view -> represents the View of this MVC project

        Methods
        -------
        start -> renvoie la position de x et y
        counter variable counts the number of "while" loops
        """


    def __init__(self):
        self.model = models.Players
        self.view = views.HomePage()

    def start(self):
        self.start = True
        counter = 0
        while self.start:
            if counter == 0:
                self.view.show_title()
            counter += 1
            self.view.show_menu()
            new_view = self.view.ask_user_choice()
            self.view = new_view

if __name__ == "__main__":
    pass
