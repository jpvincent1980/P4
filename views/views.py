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
              "8": "Retour au menu principal",
              "9": "Quitter le programme"}

SORTING_MENU = {"1": "ordre alphabétique",
                "2": "classement"}


class View:

    def __init__(self):
        pass

    @classmethod
    def show_title(cls):
        # chess_symbol = u"\u265E"
        chess_symbol = "+"
        title = "Gestionnaire de tournoi d'échecs"

        print(chess_symbol * (len(title)+6))
        print(chess_symbol * 2,
              f"{title.upper()}",
              chess_symbol * 2)
        print(chess_symbol * (len(title)+6))
        print()

    @classmethod
    def show_welcome_message(cls):
        print("Merci de bien vouloir faire votre choix parmi le menu "
              "ci-dessous:")

    @classmethod
    def back_to_homepage(cls):
        print()
        print("Tapez Entrée pour revenir au menu principal.")
        input(">>> ")


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
        description = input("Entrez une description du tournoi "
                             "-> ") or "Ma description"
        new_tournament = models.Tournaments(name=name,
                                            place=place,
                                            start_date=start_date,
                                            end_date=end_date,
                                            description=description,
                                            add_to_db=True)
        print(f"{new_tournament.name} "
              f"a été ajouté à notre base de données.")

    def ask_user_choice(self):
        self.back_to_homepage()
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
                                    ranking=ranking, add_to_db=True)
        print(f"{new_player.first_name} {new_player.family_name} "
              f"a été ajouté à notre base de données.")
        print()

    def ask_user_choice(self):
        self.back_to_homepage()
        return HomePage()


class AddPlayersToTournament(View):
    def show_menu(self):
        if models.Tournaments().check_if_any_tournament():
            print("Entrez le numéro du tournoi:")
            tournament_id = int(input(">>> ") or 0)
            if tournament_id in models.Tournaments().list_of_ids:
                tournament = models.Tournaments().instantiate_from_db(tournament_id)
                tournament.check_players()
                if tournament.tournament_nb_of_players < 8:
                    if models.Players().check_if_any_player(display2=False):
                        tournament.check_available_players()
                        print("Entrez le numéro du joueur à inscrire au", tournament.name,":")
                        player_id = int(input(">>> ") or 0)
                        tournament.add_player_to_tournament(player_id)
            else:
                print("Numéro non valide.")

    def ask_user_choice(self):
        self.back_to_homepage()
        return HomePage()


class EnterMatches(View):
    # TODO A refaire complètement
    def show_menu(self):
        if models.Tournaments().check_if_any_tournament():
            self.ask_for_tournament()
        else:
            pass

    def ask_for_tournament(self):
        print("Entrez le numéro du tournoi:")
        self.tournament_id = int(input(">>> ") or 0)
        self.tournament = models.Tournaments().instantiate_from_db(self.tournament_id)
        if self.tournament.is_empty():
            print(f"Merci d'aller inscrire plus de joueurs afin que le tournoi soit complet.")
        elif not self.tournament.is_full():
            print(f"Il n'y a que {len(self.tournament.players)} joueur(s) inscrit(s) sur 8.\n"
                  f"Merci d'aller inscrire plus de joueurs afin que le tournoi soit complet.")
        elif len(self.tournament.rounds) == 0:
            self.tournament.generate_round()
            self.ask_for_round()
        else:
            self.ask_for_round()

    def ask_for_round(self):
        print("Voici les tours non terminés pour ce tournoi:")
        for i,round in enumerate(self.tournament.rounds,start=1):
            print(i, "->", round["name"])
        print("Entrez le numéro du round:")
        self.round_id = int(input(">>> ") or 0)
        self.ask_for_match()

    def ask_for_match(self):
        matches = self.tournament.rounds[self.round_id-1]["matches"]
        if len(matches) == 0:
            self.tournament.generate_matches(self.round_id)
            matches = self.tournament.rounds[self.round_id - 1]["matches"]
        print("Voici les matchs non joués pour ce round:")
        for i,match in enumerate(matches,start=1):
            match = ([match[0][0],match[1][0]],[match[0][1],match[1][1]])
            instantiated_match = models.Matches(match)
            print(i, "->", instantiated_match)
        print("Choisissez le numéro du match:")
        self.match_id = int(input(">>> ") or 0)
        selected_match = matches[self.match_id-1]
        match = ([selected_match[0][0]],[selected_match[1][0]]])
        self.updated_match = models.Matches(match)
        self.ask_for_score()

    def ask_for_score(self):
        print(f"Entrez le score de {self.updated_match.player1['first_name']} "
              f"{self.updated_match.player1['family_name']}:")
        score_player1 = float(input(">>> "))
        print(f"Entrez le score de {self.updated_match.player2['first_name']} "
              f"{self.updated_match.player2['family_name']}:")
        score_player2 = float(input(">>> "))
        self.updated_match.match_score(score_player1,score_player2)
        self.tournament.rounds[self.round_id - 1]["matches"][self.match_id-1] = self.updated_match.pair
        models.DB.update_record_data("tournaments",self.tournament_id,"rounds",self.tournament.rounds)
        print("Le résultat du match a bien été mis à jour.")

    def ask_user_choice(self):
        self.back_to_homepage()
        return HomePage()

class EnterRankings(View):
    def show_menu(self):
        pass

    def ask_user_choice(self):
        if models.Players().check_if_any_player():
            player_id = int(input(">>> ") or 0)
            if player_id in models.Players().list_of_ids():
                player_first_name = models.DB.get_record_data("players",player_id,"first_name")
                player_family_name = models.DB.get_record_data("players",player_id,"family_name")
                print(f"Entrez le nouveau classement de {player_first_name} {player_family_name}:")
                new_ranking = input(">>> ")
                if int(new_ranking) > 0:
                    models.DB.update_record_data("players",player_id,"ranking",new_ranking)
                    print(f"Le classement de {player_first_name} {player_family_name} a bien été mis à jour.")
                else:
                    print("Le classement doit être un chiffre strictement positif.")
            else:
                print("Numéro non valide.")
        self.back_to_homepage()
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
        elif choice == "8":
            return HomePage()
        elif choice == "9":
            return EndPage()


class DisplayListPlayers(DisplayList):
    global SORTING_MENU
    def show_menu(self):
        if len(models.PLAYERS_TABLE) == 0:
            print("Aucun joueur enregistré dans la base de données.")
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

    def ask_user_choice(self):
        self.back_to_homepage()
        return HomePage()


class DisplayListPlayersByTournament(View):
    def show_menu(self):
        pass

    def ask_user_choice(self):
        if models.Tournaments().check_if_any_tournament():
            print("Merci de saisir un numéro de tournoi:")
            tournament_id = int(input(">>> ") or 0)
            if tournament_id in models.Tournaments().list_of_ids:
                tournament = models.Tournaments().instantiate_from_db(tournament_id)
                tournament.is_empty()
            else:
                print("Numéro non valide.")
        self.back_to_homepage()
        return HomePage()


class DisplayListTournaments(View):
    def show_menu(self):
        pass

    def ask_user_choice(self):
        models.Tournaments().check_if_any_tournament()
        self.back_to_homepage()
        return HomePage()


class DisplayListRoundsByTournament(View):
    def show_menu(self):
        pass

    def ask_user_choice(self):
        if models.Tournaments().check_if_any_tournament():
            print("Merci de saisir un numéro de tournoi:")
            tournament_id = int(input(">>> ") or 0)
            if tournament_id in models.Tournaments().list_of_ids:
                tournament_rounds = models.DB.get_record_data("tournaments",
                                                               int(tournament_id),
                                                               "rounds")
                tournament_name = models.DB.get_record_data("tournaments",
                                                            int(tournament_id),
                                                            "name",)
                if len(tournament_rounds) == 0:
                    print("Aucun round pour le ", tournament_name,".",sep="")
                else:
                    print("Voici les rounds du", tournament_name,":")
                    for round in tournament_rounds:
                        print(round["name"])
            else:
                print("Numéro non valide.")
        self.back_to_homepage()
        return HomePage()


class DisplayListMatchesByTournament(View):
    def show_menu(self):
        if models.Tournaments().check_if_any_tournament():
            print("Merci de saisir un numéro de tournoi:")
            tournament_id = int(input(">>> ") or 0)
            if tournament_id in models.Tournaments().list_of_ids:
                tournament = models.Tournaments().instantiate_from_db(tournament_id)
                if len(tournament.rounds) == 0 and not tournament.is_full():
                    print(f"Aucun round n'existe pour ce tournoi.\n"
                          f"Merci de vérifier qu'il y a bien 8 joueurs inscrits à ce tournoi.")
                else:
                    if tournament.nb_of_rounds == 0:
                        print("Aucun round n'existe pour ce tournoi.\n"
                              "Merci de vous assurer qu'il y a bien 8 joueurs inscrits.")
                    else:
                        print("Merci de sélectionner le round du tournoi en tapant son numéro ->")
                        for i,round in enumerate(tournament.rounds,start=1):
                            print(i, "->", round["name"])
                        round_id = int(input(">>> ") or 0)
                        matches = tournament.rounds[round_id-1]["matches"]
                        if len(matches) == 0:
                            print("Aucun match n'existe pour ce round.")
                        else:
                            matches = tournament.rounds[round_id - 1]["matches"]
                        for i,match in enumerate(matches, start=1):
                            instantiated_match = models.Matches(match)
                            print(i, "->", instantiated_match)
            else:
                print("Nuémro non valide.")
        else:
            pass

    def ask_user_choice(self):
        self.back_to_homepage()
        return HomePage()


class ExportList(View):
    def show_menu(self):
        global LISTS_MENU
        print("Choisissez une liste à exporter parmi les suivantes:")
        self.menu = LISTS_MENU
        for key in self.menu.items():
            print(key[0], ": ", key[1])

    def ask_user_choice(self):
        self.back_to_homepage()
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
