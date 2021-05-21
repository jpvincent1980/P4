#! /usr/bin/env python3
# coding: utf-8

from models import models

MAIN_MENU = {"1": "Créer un nouveau tournoi",
             "2": "Créer un nouveau joueur",
             "3": "Inscrire un joueur à un tournoi",
             "4": "Entrer les résultats d'un match",
             "5": "Entrer le classement d'un joueur",
             "6": "Afficher une liste",
             "7": "Exporter une liste",
             "9": "Quitter le programme"}

LISTS_MENU = {"1": "Liste de tous les joueurs",
              "2": "Liste de tous les joueurs d'un tournoi",
              "3": "Liste de tous les tournois",
              "4": "Liste de tous les tours d'un tournoi",
              "5": "Liste de tous les matchs d'un tournoi",
              "6": "Liste de tous les appariements",
              "8": "Retour au menu principal",
              "9": "Quitter le programme"}


class View:

    def __init__(self):
        pass

    @staticmethod
    def show_welcome_message():
        print("Bienvenue dans votre logiciel de gestion de "
              "tournois d'échecs.")
        print("Merci de bien vouloir faire votre choix parmi le menu "
              "ci-dessous:")


class HomePage(View):

    def show_menu(self):
        global MAIN_MENU
        self.menu = MAIN_MENU
        self.show_welcome_message()
        for key in self.menu.items():
            print(key[0], ": ", key[1])

    def ask_user_choice(self):
        choice = input(">>> ")
        if choice not in self.menu or choice == "0":
            print("Choix non valide. Veuillez ressaisir un choix "
                  "parmi la liste.")
            return HomePage()
        elif choice == "1":
            return Tournaments().show_menu()
        elif choice == "2":
            return AddPlayers().show_menu()
        elif choice == "3":
            return AddPlayersToTournament().show_menu()
        elif choice == "4":
            return Matches().show_menu()
        elif choice == "5":
            return Rankings().show_menu()
        elif choice == "6":
            return DisplayList().show_menu()
        elif choice == "7":
            return ExportList().show_menu()
        elif choice == "9":
            return quit()


class Tournaments(View):
    def show_menu(self):
        print("Vous allez créer un nouveau tournoi.")
        name = input("Entrez le nom du tournoi -> ")
        place = input("Entrez le lieu où se déroule le tournoi -> ")
        start_date = input("Entrez la date de début du tournoi "
                           "(JJ/MM/AAAA) -> ")
        end_date = input("Entrez la date de fin du tournoi "
                         "(JJ/MM/AAAA) -> ")
        nb_of_rounds = input("Entrez le nombre de tours du tournoi "
                             "-> ")
        new_tournament = models.Tournaments(name=name,
                                            place=place)
        print(f"Le tournoi {new_tournament.name} se déroule à "
              f"{new_tournament.place} en mode {new_tournament.time_control}.")
        input()


class Players(View):
    def show_menu(self):
        print("Afficher la liste des joueurs par :")
        print("1: Ordre alphabétique")
        print("2: Classement")
        choice = input(">>> ")
        if choice == "1":
            players = sorted(models.Players.all_players,
                             key=lambda x: x.family_name)
            if len(players) < 1:
                print("Aucun joueur n'est renseigné dans la base de données.")
            for player in players:
                print(player.first_name, " ", player.family_name,
                      " - Classement -> ", player.ranking)
            input(">>> ")
        elif choice == "2":
            players = sorted(models.Players.all_players,
                             key=lambda x: x.ranking)
            if len(players) < 1:
                print("Aucun joueur n'est renseigné dans la base de données.")
            for player in players:
                print(player.first_name, " ", player.family_name,
                      " - Classement -> ", player.ranking)
            input(">>> ")
        else:
            print("Choix non valide.")
            return Players.show_menu(self)


class PlayersByTournament(View):
    def show_menu(self):
        tournament = input("Entrez le nom du tournoi:")
        if tournament not in models.Tournaments.all_tournaments:
            print("Ce tournoi n'existe pas.")
        else:
            print("Les joueurs inscrit au tournoi " + tournament + " sont:")


class AddPlayers(View):
    def show_menu(self):
        print("Vous allez créer un nouveau joueur.")
        first_name = input("Entrez le prénom du joueur -> ")
        family_name = input("Entrez le nom du joueur -> ")
        birth_date = input("Entrez la date de naissance du joueur "
                           "(JJ/MM/AAAA) -> ")
        sex = input("Entrez le sexe du joueur (H/F) -> ")
        ranking = input("Entrez le classement du joueur -> ")
        new_player = models.Players(first_name=first_name,
                                    family_name=family_name,
                                    birth_date=birth_date,
                                    sex=sex,
                                    ranking=ranking)
        print(f"{new_player.first_name} {new_player.family_name} "
              f"a été ajouté à notre base de joueurs.")
        input()


class AddPlayersToTournament(View):
    def show_menu(self):
        choice = input("Entrez le nom du tournoi: ")
        for tournament in models.Tournaments.all_tournaments:
            if tournament.name == choice:
                print("Nombre de joueurs déjà inscrit au tournoi",
                      choice,
                      ":",
                      len(tournament.players))
                tournament.players.append(Players())
                break
            else:
                continue


class Matches(View):
    def ask_for_tournament(self):
        print("Veuillez entrer le nom du tournoi:")
        tournament = input(">>> ")
        if tournament not in models.Tournaments.all_tournaments:
            print("Ce tournoi n'existe pas.")
            print("Merci de saisir le nom d'un des tournois ci-dessous")
            for i, tournament in enumerate(models.Tournaments.all_tournaments,
                                           start=1):
                print(i, ": ", tournament)
            self.ask_for_tournament()
        else:
            self.tournament = models.Tournaments(name=tournament)
            self.ask_for_round()

    def ask_for_round(self):
        print("Voici les tours non terminés pour ce tournoi:")
        for round in self.tournament.rounds:
            print(round)
            input()

    def show_menu(self):
        self.ask_for_tournament()


class Rankings(View):
    def show_menu(self):
        print("This is the Rankings view.")


class DisplayList(View):
    def show_menu(self):
        global LISTS_MENU
        print("Choisissez une liste à afficher parmi les suivantes:")
        self.menu = LISTS_MENU
        for key in self.menu.items():
            print(key[0], ": ", key[1])
        choice = input()
        if choice == "1":
            return Players().show_menu()
        if choice == "2":
            return PlayersByTournament().show_menu()
        if choice == "3":
            if len(models.Tournaments.all_tournaments) < 1:
                print("Aucun tournoi n'est renseigné dans "
                      "la base de données")
            else:
                print("Voici la liste des tournois existants:")
                for i, tournament in \
                        enumerate(models.Tournaments.all_tournaments, start=1):
                    print(i, ": ", tournament.name)
                print()
            print("Tapez Entrée pour revenir au menu principal")
            input(">>> ")
        return HomePage()


class ExportList(View):
    def show_menu(self):
        global LISTS_MENU
        print("Choisissez une liste à exporter parmi les suivantes:")
        self.menu = LISTS_MENU
        for key in self.menu.items():
            print(key[0], ": ", key[1])
        choice = input()


if __name__ == "__main__":
    pass
