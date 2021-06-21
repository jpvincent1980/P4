#! /usr/bin/env python3
# coding: utf-8
from views import views as views


class NoTournament(views.View):
    """
    A class that displays a warning message to user

        Attributes
        ----------
            None

        Methods
        -------
            show_message -> prints a message to user
            ask_user_choice -> asks user to press Enter to go back to HomePage
    """
    def show_message(self):
        """
        Prints message to user
        """
        print(f"Aucun tournoi n'est créé dans la base de données.")

    def ask_user_choice(self):
        """
        Asks user to press Enter to go back to HomePage
        """
        self.back_to_homepage()
        return views.HomePage()


class NoOpenTournament(views.View):
    """
    A class that displays a warning message to user

        Attributes
        ----------
            None

        Methods
        -------
            show_message -> prints a message to user
            ask_user_choice -> asks user to press Enter to go back to HomePage
    """
    def show_message(self):
        """
        Prints message to user
        """
        print(f"Aucun tournoi n'est actuellement en cours.")

    def ask_user_choice(self):
        """
        Asks user to press Enter to go back to HomePage
        """
        self.back_to_homepage()
        return views.HomePage()
    

class UnknownTournament(views.View):
    """
    A class that displays a warning message to user

        Attributes
        ----------
            None

        Methods
        -------
            show_message -> prints a message to user
            ask_user_choice -> asks user to press Enter to go back to HomePage
    """
    def show_message(self):
        """
        Prints message to user
        """
        print(f"Numéro de tournoi non valide.\n")

    def ask_user_choice(self):
        """
        Asks user to press Enter to go back to HomePage
        """
        self.back_to_homepage()
        return views.HomePage()


class UnknownPlayer(views.View):
    """
    A class that displays a warning message to user

        Attributes
        ----------
            None

        Methods
        -------
            show_message -> prints a message to user
            ask_user_choice -> asks user to press Enter to go back to HomePage
    """
    def show_message(self):
        """
        Prints message to user
        """
        print(f"Numéro de joueur non valide.\n")

    def ask_user_choice(self):
        """
        Asks user to press Enter to go back to HomePage
        """
        self.back_to_homepage()
        return views.HomePage()


class UnknownRound(views.View):
    """
    A class that displays a warning message to user

        Attributes
        ----------
            None

        Methods
        -------
            show_message -> prints a message to user
            ask_user_choice -> asks user to press Enter to go back to HomePage
    """
    def show_message(self):
        """
        Prints message to user
        """
        print(f"Numéro de round non valide.\n")

    def ask_user_choice(self):
        """
        Asks user to press Enter to go back to HomePage
        """
        self.back_to_homepage()
        return views.HomePage()


class UnknownMatch(views.View):
    """
    A class that displays a warning message to user

        Attributes
        ----------
            None

        Methods
        -------
            show_message -> prints a message to user
            ask_user_choice -> asks user to press Enter to go back to HomePage
    """
    def show_message(self):
        """
        Prints message to user
        """
        print(f"Numéro de match non valide.\n")

    def ask_user_choice(self):
        """
        Asks user to press Enter to go back to HomePage
        """
        self.back_to_homepage()
        return views.HomePage()


class NoPlayer(views.View):
    """
    A class that displays a warning message to user

        Attributes
        ----------
            None

        Methods
        -------
            show_message -> prints a message to user
            ask_user_choice -> asks user to press Enter to go back to HomePage
    """
    def show_message(self):
        """
        Prints message to user
        """
        print(f"Aucun joueur n'est créé dans la base de données.\n")

    def ask_user_choice(self):
        """
        Asks user to press Enter to go back to HomePage
        """
        self.back_to_homepage()
        return views.HomePage()


class NoPlayersEnlistedView(views.View):
    """
    A class that displays a warning message to user

        Attributes
        ----------
            None

        Methods
        -------
            show_message -> prints a message to user
            ask_user_choice -> asks user to press Enter to go back to HomePage
    """
    def show_message(self):
        """
        Prints message to user
        """
        print(f"Aucun joueur n'est inscrit à ce tournoi.\n")

    def ask_user_choice(self):
        """
        Asks user to press Enter to go back to HomePage
        """
        self.back_to_homepage()
        return views.HomePage()


class PlayerAlreadyEnlisted(views.View):
    """
    A class that displays a warning message to user

        Attributes
        ----------
            None

        Methods
        -------
            show_message -> prints a message to user
            ask_user_choice -> asks user to press Enter to go back to HomePage
    """
    def show_message(self):
        """
        Prints message to user
        """
        print(f"Ce joueur est déjà inscrit à ce tournoi.\n")

    def ask_user_choice(self):
        """
        Asks user to press Enter to go back to HomePage
        """
        self.back_to_homepage()
        return views.HomePage()


class IncorrectScoresView(views.View):
    """
    A class that displays a warning message to user

        Attributes
        ----------
            None

        Methods
        -------
            show_message -> prints a message to user
            ask_user_choice -> asks user to press Enter to go back to HomePage
    """
    def show_message(self):
        """
        Prints message to user
        """
        print(f"La somme des points attribués doit être égale à 1.\n"
              f"Les points attribuables ne peuvent être que: "
              f"{mt.POINTS_LIST}\n")

    def ask_user_choice(self):
        """
        Asks user to press Enter to go back to HomePage
        """
        self.back_to_homepage()
        return views.HomePage()


class InvalidChoiceView(views.View):
    """
    A class that displays a warning message to user

        Attributes
        ----------
            None

        Methods
        -------
            show_message -> prints a message to user
            ask_user_choice -> asks user to press Enter to go back to HomePage
    """
    def show_message(self):
        """
        Prints message to user
        """
        print(f"Choix non valide.\n"
              f"Veuillez ressaisir un choix parmi la liste.\n")

    def ask_user_choice(self):
        """
        Asks user to press Enter to go back to HomePage
        """
        self.back_to_homepage()
        return views.HomePage()


class NoRound(views.View):
    """
    A class that displays a warning message to user

        Attributes
        ----------
            None

        Methods
        -------
            show_message -> prints a message to user
            ask_user_choice -> asks user to press Enter to go back to HomePage
    """
    def show_message(self):
        """
        Prints message to user
        """
        print(f"Aucun round n'existe pour ce tournoi.\n"
              f"Vérifiez le nombre de joueurs inscrits.")

    def ask_user_choice(self):
        """
        Asks user to press Enter to go back to HomePage
        """
        self.back_to_homepage()
        return views.HomePage()


class CompletedRound(views.View):
    """
    A class that displays a warning message to user

        Attributes
        ----------
            None

        Methods
        -------
            show_message -> prints a message to user
            ask_user_choice -> asks user to press Enter to go back to HomePage
    """
    def show_message(self):
        """
        Prints message to user
        """
        print(f"Ce round est terminé.\n")

    def ask_user_choice(self):
        """
        Asks user to press Enter to go back to HomePage
        """
        self.back_to_homepage()
        return views.HomePage()


class NoMatch(views.View):
    """
    A class that displays a warning message to user

        Attributes
        ----------
            None

        Methods
        -------
            show_message -> prints a message to user
            ask_user_choice -> asks user to press Enter to go back to HomePage
    """
    def show_message(self):
        """
        Prints message to user
        """
        print(f"Aucun match n'existe pour ce tournoi.\n"
              f"Vérifiez le nombre de joueurs inscrits.")

    def ask_user_choice(self):
        """
        Asks user to press Enter to go back to HomePage
        """
        self.back_to_homepage()
        return views.HomePage()


class CompletedMatch(views.View):
    """
    A class that displays a warning message to user

        Attributes
        ----------
            None

        Methods
        -------
            show_message -> prints a message to user
            ask_user_choice -> asks user to press Enter to go back to HomePage
    """
    def show_message(self):
        """
        Prints message to user
        """
        print(f"Ce match est terminé.\n")

    def ask_user_choice(self):
        """
        Asks user to press Enter to go back to HomePage
        """
        self.back_to_homepage()
        return views.HomePage()


class InactiveTournament(views.View):
    """
    A class that displays a warning message to user

        Attributes
        ----------
            None

        Methods
        -------
            show_message -> prints a message to user
            ask_user_choice -> asks user to press Enter to go back to HomePage
    """
    def show_message(self):
        """
        Prints message to user
        """
        print(f"Ce tournoi n'a pas démarré ou est terminé.\n")

    def ask_user_choice(self):
        """
        Asks user to press Enter to go back to HomePage
        """
        self.back_to_homepage()
        return views.HomePage()