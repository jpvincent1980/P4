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
    def show_title():
        # chess_symbol = u"\u265E"
        chess_symbol = "+"
        title = "Gestionnaire de tournoi d'échecs"

        print(chess_symbol * (len(title)+6))
        print(chess_symbol * 2,
              f"{title.upper()}",
              chess_symbol * 2)
        print(chess_symbol * (len(title)+6))
        print()

    @staticmethod
    def show_welcome_message():
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
        if choice not in self.menu:
            print("Choix non valide. Veuillez ressaisir un choix "
                  "parmi la liste.")
            return HomePage()
        elif choice == "1":
            return CreateTournament()
        elif choice == "2":
            return CreatePlayer()
        elif choice == "3":
            return AddPlayersToTournament()
        elif choice == "4":
            return EnterMatches()
        elif choice == "5":
            return EnterRankings()
        elif choice == "6":
            return DisplayList()
        elif choice == "7":
            return ExportList()
        elif choice == "9":
            return EndPage()


class CreateTournament(View):
    def show_menu(self):
        print("Vous allez créer un nouveau tournoi.")
        name = input("Entrez le nom du tournoi -> ")
        place = input("Entrez le lieu où se déroule le tournoi -> ") or "Paris"
        start_date = input("Entrez la date de début du tournoi "
                           "(JJ/MM/AAAA) -> ") or "14/10/1980"
        end_date = input("Entrez la date de fin du tournoi "
                         "(JJ/MM/AAAA) -> ") or "14/10/1980"
        nb_of_rounds = input("Entrez le nombre de tours du tournoi "
                             "-> ") or "4"
        new_tournament = models.Tournaments(name=name,
                                            place=place,
                                            start_date=start_date,
                                            end_date=end_date,
                                            nb_of_rounds=nb_of_rounds)
        print(f"{new_tournament.name} "
              f"a été ajouté à notre base de données.")

    def ask_user_choice(self):
        input("Appuyez sur Entrée pour retourner au menu principal >>> ")
        return HomePage()


class CreatePlayer(View):
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
              f"a été ajouté à notre base de données.")
        print()

    def ask_user_choice(self):
        input("Appuyez sur Entrée pour retourner au menu principal >>> ")
        return HomePage()


class AddPlayersToTournament(View):
    def show_menu(self):
        choice = input("Entrez le nom du tournoi: ")
        for tournament in models.TOURNAMENTS_TABLE:
            if tournament.name == choice:
                print("Nombre de joueurs déjà inscrit au tournoi",
                      choice,
                      ":",
                      len(TOURNAMENTS_TABLE))
                tournament.players.append(Players())
                break
            else:
                continue

    def ask_user_choice(self):
        return HomePage()


class EnterMatches(View):
    def show_menu(self):
        self.ask_for_tournament()

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

    def ask_user_choice(self):
        return HomePage()

class EnterRankings(View):
    def show_menu(self):
        print("This is the Rankings view.")

    def ask_user_choice(self):
        return HomePage()


class DisplayList(View):
    def show_menu(self):
        global LISTS_MENU
        print("Choisissez une liste à afficher parmi les suivantes:")
        self.menu = LISTS_MENU
        for key in self.menu.items():
            print(key[0], ": ", key[1])

    def ask_user_choice(self):
        choice = input(">>> ")
        if choice not in self.menu:
            print("Choix non valide. Veuillez ressaisir un choix "
                  "parmi la liste.")
            return DisplayList()
        elif choice == "1":
            return DisplayListPlayers()
        elif choice == "2":
            return DisplayListPlayersByTournament()
        elif choice == "3":
            return DisplayListTournaments()
        elif choice == "4":
            return DisplayListRoundsByTournament()
        elif choice == "5":
            return DisplayListMatchesByTournament()
        elif choice == "6":
            return DisplayListPairings()
        elif choice == "8":
            return HomePage()
        elif choice == "9":
            return EndPage()


class DisplayListPlayers(View):
    def show_menu(self):
        if len(models.PLAYERS_TABLE) == 0:
            print("Aucun joueur enregistré dans la base de données.")
            print("Tapez Entrée pour revenir au menu principal.")
        else:
            print("Voici la liste des joueurs enregistrés:")
            for player in models.PLAYERS_TABLE:
                print(player.doc_id,"->",player["first_name"],player["family_name"])
            print()

    def ask_user_choice(self):
        print("Tapez Entrée pour revenir au menu principal.")
        input(">>> ")
        return HomePage()


class DisplayListPlayersByTournament(View):
    def show_menu(self):
        print("Merci de sélectionner le tournoi en tapant son numéro ->")
        for tournament in models.TOURNAMENTS_TABLE:
            print(tournament.doc_id, "->", tournament["name"])

    def ask_user_choice(self):
        tournament_number = input(">>> ")
        nb_of_players = models.TOURNAMENTS_TABLE.get(doc_id=int(tournament_number))["players"]
        tournament_name = models.TOURNAMENTS_TABLE.get(doc_id=int(tournament_number))["name"]
        if len(nb_of_players) == 0:
            print("Aucun joueur n'est inscrit au", tournament_name,":")
            print()
            print("Tapez Entrée pour revenir au menu principal.")
            input(">>> ")
        else:
            print("Voici les inscrits au", tournament_name,":")
            for player in nb_of_players:
                print(player["first_name"],player["family_name"])
            print()
            print("Tapez Entrée pour revenir au menu principal.")
            input(">>> ")
        return HomePage()


class DisplayListTournaments(View):
    def show_menu(self):
        if len(models.TOURNAMENTS_TABLE) == 0:
            print("Aucun tournoi enregistré dans la base de données.")
            print("Tapez Entrée pour revenir au menu principal.")
        else:
            print("Voici la liste des tournois enregistrés:")
            for tournament in models.TOURNAMENTS_TABLE:
                print(tournament.doc_id,"->",tournament["name"])
            print("Tapez Entrée pour revenir au menu principal.")

    def ask_user_choice(self):
        choice = input(">>> ")
        return HomePage()


class DisplayListRoundsByTournament(View):
    def show_menu(self):
        pass

    def ask_user_choice(self):
        choice = input(">>> ")
        return HomePage()


class DisplayListMatchesByTournament(View):
    def show_menu(self):
        pass

    def ask_user_choice(self):
        choice = input(">>> ")
        return HomePage()


class DisplayListPairings(View):
    def show_menu(self):
        pass

    def ask_user_choice(self):
        choice = input(">>> ")
        return HomePage()


class ExportList(View):
    def show_menu(self):
        global LISTS_MENU
        print("Choisissez une liste à exporter parmi les suivantes:")
        self.menu = LISTS_MENU
        for key in self.menu.items():
            print(key[0], ": ", key[1])

    def ask_user_choice(self):
        return HomePage()


class EndPage(View):
    def show_menu(self):
        # chess_symbol = u"\u265E"
        chess_symbol = "+"
        message = "A bientôt !"

        print()
        print(chess_symbol * (len(message) + 6))
        print(chess_symbol * 2,
              f"{message.upper()}",
              chess_symbol * 2)
        print(chess_symbol * (len(message) + 6))
        print()
        quit()

if __name__ == "__main__":
    pass
