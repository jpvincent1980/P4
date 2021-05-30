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

SORTING_MENU = {"1": "ordre alphabétique",
                "2": "classement"}


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
                           "(JJ/MM/AAAA) -> ") or models.TODAY
        end_date = input("Entrez la date de fin du tournoi "
                         "(JJ/MM/AAAA) -> ") or models.TODAY
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
        print("Voici la liste des tournois enregistrés:")
        for tournament in models.TOURNAMENTS_TABLE:
            print(tournament.doc_id, "->", tournament["name"])
        print("Entrez le numéro du tournoi:")
        tournament_id = int(input(">>> "))
        tournament_name = models.DB.get_record_data("tournaments",
                                                    tournament_id,
                                                    "name")
        tournament_players = models.DB.get_record_data("tournaments",
                                                       tournament_id,
                                                       "players")
        tournament_nb_of_players = len(models.DB.get_record_data("tournaments",
                                                       tournament_id))
        tournament_players_id = []
        if tournament_nb_of_players == 0:
            print("Aucun joueur n'est inscrit au", tournament_name, "pour le moment.")
        elif len(tournament_players) >= 8:
            print("Le tournoi est déjà complet avec les joueurs suivants:")
            for player in tournament_players:
                print(player["first_name"],player["family_name"])
            return
        else:
            print("Voici la liste des joueurs déjà inscrits au", tournament_name, ":")
            for player in tournament_players:
                print(player["first_name"],player["family_name"])
                tournament_players_id.append(player["id"])
        print()

        all_players_id = []
        for player in models.PLAYERS_TABLE.all():
            all_players_id.append(player.doc_id)
        unregistered_players_id = list(set(all_players_id).difference(tournament_players_id))

        if len(unregistered_players_id) == 0 and tournament_nb_of_players > 0:
            print("Tous les joueurs de la base sont déjà inscrits au", tournament_name, end=".\n")
            print("Merci de créer un nouveau joueur avant de l'inscrire au", tournament_name, end=".\n")
        else:
            print("Voici la liste des joueurs enregistrés non inscrits au", tournament_name, ":")
            for player in models.PLAYERS_TABLE:
                if player.doc_id not in tournament_players_id:
                    print(player.doc_id, "->", player["first_name"], player["family_name"])
            print("Entrez le numéro du joueur à inscrire au", tournament_name,":")
            player_id = int(input(">>> "))
            if player_id in tournament_players_id:
                print("Ce joueur est déjà inscrit au", tournament_name, ".")
            elif player_id not in unregistered_players_id:
                print("Choix non valide.")
            else:
                serialized_player = models.DB.get_record_data("players", player_id)
                serialized_player.update({"id": player_id})
                models.DB.update_record_data("tournaments", "players", serialized_player, tournament_id, True)
                # models.add_players(tournament_id, player_id)
                player_first_name = models.DB.get_record_data("players",
                                                    player_id,
                                                    "first_name")
                player_family_name = models.DB.get_record_data("players",
                                                    player_id,
                                                    "family_name")
                print(f"{player_first_name} {player_family_name} a été inscrit au {tournament_name}.")

    def ask_user_choice(self):
        print()
        input("Appuyez sur Entrée pour retourner au menu principal >>> ")
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
        if len(models.PLAYERS_TABLE) == 0:
            print("Aucun joueur n'est enregistré dans la base de données.")
            print("Tapez Entrée pour revenir au menu principal.")
        else:
            print("Entrez le numéro du joueur:")
            for player in models.PLAYERS_TABLE:
                print(player.doc_id,"->",player["first_name"],player["family_name"],
                      "| Classement actuel ->", player["ranking"])
            print()
            player_id = int(input(">>> "))
            player_first_name = models.DB.get_record_data("players",player_id,"first_name")
            player_family_name = models.DB.get_record_data("players",player_id,"family_name")
            print(f"Entrez le nouveau classement de {player_first_name} {player_family_name}:")
            new_ranking = input(">>> ")
            models.DB.update_record_data("players","ranking",new_ranking,player_id)

    def ask_user_choice(self):
        print()
        print("Tapez Entrée pour revenir au menu principal.")
        input(">>> ")
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


class DisplayListPlayers(DisplayList):
    global SORTING_MENU
    def show_menu(self):
        if len(models.PLAYERS_TABLE) == 0:
            print("Aucun joueur enregistré dans la base de données.")
            print("Tapez Entrée pour revenir au menu principal.")
        else:
            print("Affichez la liste des joueurs par:")
            for element in SORTING_MENU.items():
                print(element[0],":",element[1])
            ranking_sort = input(">>> ")
            print("Voici la liste des joueurs enregistrés:")
            if ranking_sort == "1":
                for player in sorted(models.PLAYERS_TABLE, key=lambda x:x['family_name']):
                    print(player["first_name"],
                          player["family_name"],
                          "| Classement -> n°",
                          player["ranking"])
            elif ranking_sort == "2":
                for player in sorted(models.PLAYERS_TABLE, key=lambda x:int(x['ranking'])):
                    print(player["first_name"],
                          player["family_name"],
                          "| Classement -> n°",
                          player["ranking"])
            else:
                print("Choix non valide.")
                return
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
        tournament_id = input(">>> ")
        tournament_players = models.DB.get_record_data("tournaments",
                                                       int(tournament_id),
                                                       "players")
        tournament_name = models.DB.get_record_data("tournaments",
                                                    int(tournament_id),
                                                    "name",)
        if len(tournament_players) == 0:
            print("Aucun joueur n'est inscrit au ", tournament_name,".",sep="")
            print()
            print("Tapez Entrée pour revenir au menu principal.")
            input(">>> ")
        else:
            print("Voici les inscrits au", tournament_name,":")
            for player in tournament_players:
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
        print("Merci de sélectionner le tournoi en tapant son numéro ->")
        for tournament in models.TOURNAMENTS_TABLE:
            print(tournament.doc_id, "->", tournament["name"])

    def ask_user_choice(self):
        tournament_id = input(">>> ")
        tournament_rounds = models.DB.get_record_data("tournaments",
                                                       int(tournament_id),
                                                       "rounds")
        tournament_name = models.DB.get_record_data("tournaments",
                                                    int(tournament_id),
                                                    "name",)
        if len(tournament_rounds) == 0:
            print("Aucun round pour le ", tournament_name,".",sep="")
            print()
            print("Tapez Entrée pour revenir au menu principal.")
            input(">>> ")
        else:
            print("Voici les rounds du", tournament_name,":")
            for round in tournament_rounds:
                print(round["name"])
            print()
            print("Tapez Entrée pour revenir au menu principal.")
            input(">>> ")
        return HomePage()


class DisplayListMatchesByTournament(View):
    def show_menu(self):
        DisplayListRoundsByTournament().show_menu()
        tournament_id = input(">>> ")
        tournament_rounds = models.DB.get_record_data("tournaments",
                                                      int(tournament_id),
                                                      "rounds")
        print("Merci de sélectionner le round du tournoi en tapant son numéro ->")
        for i,round in enumerate(tournament_rounds,start=1):
            print(i, "->", round["name"])
        round_id = input(">>> ")
        for match in tournament_rounds[int(round_id)-1]["matches"]:
            print(match)

    def ask_user_choice(self):
        input(">>> ")
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
