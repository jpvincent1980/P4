#! /usr/bin/env python3
# coding: utf-8
from controllers import controller as ct
from models import player as pl
from models import tournament as tr
from models import round as rn
from models import match as mt


SORTING_MENU = {"1": "Ordre alphabétique",
                "2": "Classement"}


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
        return HomePage()


class HomePage(View):
    def show_menu(self):
        self.menu = ct.MAIN_MENU
        self.show_welcome_message()
        for key in self.menu.items():
            print(key[0], ": ", key[1])

    def ask_user_choice(self):
        return input(">>> ")


class NoTournament(View):
    def show_menu(self):
        print("Aucun tournoi n'est créé dans la base de données.")

    def ask_user_choice(self):
        self.back_to_homepage()
        return HomePage()


class UnknownTournament(View):
    def show_menu(self):
        print("Numéro de tournoi non valide.")

    def ask_user_choice(self):
        self.back_to_homepage()
        return HomePage()


class NoPlayer(View):
    def show_menu(self):
        print("Aucun joueur n'est créé dans la base de données.")

    def ask_user_choice(self):
        self.back_to_homepage()
        return HomePage()


class UnknownPlayer(View):
    def show_menu(self):
        print("Numéro de joueur non valide.")

    def ask_user_choice(self):
        self.back_to_homepage()
        return HomePage()


class CreateTournamentView(View):
    def show_menu(self):
        print("Vous allez créer un nouveau tournoi.")

    def ask_user_choice(self):
        self.name = input("Entrez le nom du tournoi -> ")
        self.place = input("Entrez le lieu où se déroule le tournoi -> ")
        self.time_control = input(f"Entrez le numéro du type de contrôle du temps :\n"
                             f"{tr.TIME_CONTROL}\n"
                             f">>> ")
        self.description = input("Entrez une description du tournoi "
                             "-> ")
        return


class TournamentCreationValidationView(View):
    def __init__(self,tournament_name):
        self.tournament_name = tournament_name

    def show_menu(self):
        print(f"{self.tournament_name} a bien été créé dans notre base.")

    def ask_user_choice(self):
        self.back_to_homepage()
        return HomePage()


class CreatePlayerView(View):
    def show_menu(self):
        print("Vous allez créer un nouveau joueur.")


    def ask_user_choice(self):
        self.first_name = input("Entrez le prénom du joueur -> ")
        self.family_name = input("Entrez le nom du joueur -> ")
        self.birth_date = input("Entrez la date de naissance du joueur "
                           "(JJ/MM/AAAA) -> ")
        self.sex = input("Entrez le sexe du joueur (H/F) -> ")
        self.ranking = input("Entrez le classement du joueur -> ")
        return


class PlayerCreationValidationView(View):
    def __init__(self,player_full_name):
        self.player_full_name = player_full_name

    def show_menu(self):
        print(f"{self.player_full_name} a bien été créé dans notre base.")

    def ask_user_choice(self):
        self.back_to_homepage()
        return HomePage()


class AddPlayerToTournamentView(View):
    def show_menu(self):
        print(f"Choisissez un tournoi parmi les suivants:")
        for id,name in tr.Tournament.available_tournaments().items():
            print(f"{id} -> {name}")

    def ask_user_choice(self):
        self.tournament_id = int(input(">>> ") or 0)
        return self.tournament_id


class DisplayAvailablePlayers(View):
    def __init__(self, liste):
        self.players_available_ids = liste

    def show_menu(self):
        print(f"Choisissez un joueur parmi les suivants:")
        for id in self.players_available_ids:
            print(f"{id} -> {pl.DB.get_record_data('players',id)['first_name']} "
                  f"{pl.DB.get_record_data('players',id)['family_name']}")

    def ask_user_choice(self):
        self.player_id = int(input(">>> ") or 0)
        return self.player_id


class AddPlayerValidationView(View):
    def __init__(self,player_full_name,tournament_name):
        self.player_full_name = player_full_name
        self.tournament_name = tournament_name

    def show_menu(self):
        print(f"{self.player_full_name} a bien été inscrit au {self.tournament_name}.")

    def ask_user_choice(self):
        self.back_to_homepage()
        return HomePage()


class EnterMatchScoreView(View):
    def show_menu(self):
        print(f"Choisissez un tournoi parmi les suivants:")
        for tournament in tr.Tournament.full_tournaments():
            print(f"{tournament['_id']} -> {tournament['name']}")

    def ask_user_choice(self):
        self.tournament_id = int(input(">>> ") or 0)
        return self.tournament_id


class DisplayAvailableRounds(View):
    def __init__(self,tournament):
        self.tournament = tournament

    def show_menu(self):
        print(f"Choisissez un round parmi les suivants:")
        for round in self.tournament.rounds:
            print(f"{round['name'][-1]} -> {round['name']}")

    def ask_user_choice(self):
        self.round_id = int(input(">>> ") or 0)
        return self.round_id

class DisplayAvailableMatches(View):
    def __init__(self, tournament, round_id):
        self.tournament = tournament
        self.round_id = round_id - 1

    def show_menu(self):
        print(f"Choisissez un match parmi les suivants:")
        for i,match in enumerate(self.tournament.rounds[self.round_id]["matches"],start=1):
            match = mt.Match(match)
            print(f"{i} -> {match}")

    def ask_user_choice(self):
        self.match_id = int(input(">>> ") or 0)
        return self.match_id

class EnterMatchScoresView(View):
    def __init__(self, tournament, round_id, match_id):
        self.tournament = tournament
        self.round_id = round_id - 1
        self.match_id = match_id

    def show_menu(self):
        print(f"Entrez les scores du match {self.match_id}:")

    def ask_user_choice(self):
        return

    def zask_for_score(self):
        selected_match = self.round["matches"][self.match_id-1]
        self.match = mt.Match(selected_match)
        player1 = self.match._player1["first_name"] + " " + self.match._player1["family_name"]
        player2 = self.match._player2["first_name"] + " " + self.match._player2["family_name"]
        print(f"Entrez le score de {player1} :")
        score_player1 = float(input(">>> ") or 0)
        print(f"Entrez le score de {player2}:")
        score_player2 = float(input(">>> ") or 0)
        if (score_player1 and score_player2) in mt.POINTS_LIST and \
                score_player1 + score_player2 == 1:
            self.match.match_score(score_player1,score_player2)
            if self.match_id == 4:
                self.tournament.rounds[self.round_id-1]["_end_date"] = rn.TODAY
                self.tournament.rounds[self.round_id-1]["_end_time"] = rn.NOW
            self.round.matches[self.match_id-1] = self.match.pair
            tr.DB.update_record_data("tournaments",self.tournament_id,"rounds",self.tournament.rounds)
            print("Le résultat du match a bien été mis à jour.")
            self.tournament.check_status()
        else:
            print(f"La somme des points attribués doit être égale à 1.\n"
                  f"Les points attribuables ne peuvent être que: "
                  f"{(mt.POINTS_LIST)}")


class EnterMatchScoresValidationView(View):
    def show_menu(self):
        pass

    def ask_user_choice(self):
        pass


class EnterPlayerRankingView(View):
    def show_menu(self):
        print("Entrez le numéro d'un des joueurs ci-dessous:\n")
        print(f"{'#':^4}{'Prénom':^20}{'Nom':^20}{'H/F':^10}{'Classement':^10}")
        print("+" * 70)
        for player in pl.PLAYERS_TABLE:
            print(f"{player.doc_id:^4}{player['first_name']:^20}{player['family_name']:^20}"
                  f"{player['_sex']:^10}{player['_ranking']:^10}")
        print()

    def ask_user_choice(self):
        self.player_id = int(input(">>> ") or 0)
        return self.player_id


class EnterNewRankingView(View):
    def __init__(self,player_full_name,old_ranking):
        self.player_full_name = player_full_name
        self.old_ranking = old_ranking

    def show_menu(self):
        print(f"Entrez le nouveau classement de {self.player_full_name}:")

    def ask_user_choice(self):
        self.new_ranking = input(">>> ") or 0
        print(f"Le classement de {self.player_full_name} a été mis à jour:\n"
              f"Ancien classement -> {self.old_ranking}\n"
              f"Nouveau classement -> {self.new_ranking}")
        self.back_to_homepage()
        return self.new_ranking


class DisplayList(View):
    def show_menu(self):
        print("Choisissez une liste à afficher parmi les suivantes:")
        self.menu = ct.LISTS_MENU
        for key in self.menu.items():
            print(key[0], ": ", key[1])

    def ask_user_choice(self):
        return input(">>> ")


class DisplayListPlayers(View):
    global SORTING_MENU
    def show_menu(self):
        print("Affichez la liste des joueurs par:")
        for element in SORTING_MENU.items():
            print(element[0],":",element[1])
        return

    def ask_user_choice(self):
        ranking_sort = input(">>> ")
        return ranking_sort


class DisplayListPlayersResults(View):
    def __init__(self,players_list):
        self.players_list = players_list

    def show_menu(self):
        print(f"Voici la liste des joueurs enregistrés:\n")
        print(f"{'#':^4}{'Prénom':^20}{'Nom':^20}{'Date de Naissance':^20}{'H/F':^6}{'Classement':^10}")
        print("+" * 80)
        for i,player in enumerate(self.players_list,start=1):
            print(f"{i:^4}{player['first_name']:^20}{player['family_name']:^20}"
                  f"{player['_birth_date']:^20}{player['_sex']:^6}{player['_ranking']:^10}")
        return

    def ask_user_choice(self):
        self.back_to_homepage()
        return HomePage()


class DisplayListPlayersByTournament(View):
    def show_menu(self):
        pass

    def ask_user_choice(self):
        print("Merci de saisir un numéro de tournoi:")
        tournament_id = int(input(">>> ") or 0)
        if tournament_id in tr.Tournament().list_of_ids:
            tournament = tr.Tournament().instantiate_from_db(tournament_id)
            if not tournament.is_empty(display2=False):
                print("Affichez la liste des joueurs par:")
                for element in SORTING_MENU.items():
                    print(element[0], ":", element[1])
                ranking_sort = input(">>> ")
                print("Voici la liste des joueurs inscrits au tournoi:\n")
                print(f"{'Prénom':^20}{'Nom':^20}{'Date de Naissance':^20}{'H/F':^6}{'Classement':^10}")
                print("+" * 80)
                if ranking_sort == "1":
                    for player in sorted(tournament.players, key=lambda x: x['family_name']):
                        print(f"{player['first_name']:^20}{player['family_name']:^20}"
                              f"{player['_birth_date']:^20}{player['_sex']:^6}{player['_ranking']:^10}")
                elif ranking_sort == "2":
                    for player in sorted(tournament.players, key=lambda x: int(x['_ranking'])):
                        print(f"{player['first_name']:^20}{player['family_name']:^20}"
                              f"{player['_birth_date']:^20}{player['_sex']:^6}{player['_ranking']:^10}")
        self.back_to_homepage()
        return HomePage()


class DisplayListPlayersByTournamentResults(View):
    def show_menu(self):
        pass

    def ask_user_choice(self):
        pass


class DisplayListTournaments(View):
    def show_menu(self):
        pass

    def ask_user_choice(self):
        pass


class DisplayListTournamentsResults(View):
    def __init__(self,tournaments_list):
        self.tournaments_list = tournaments_list

    def show_menu(self):
        print("Voici la liste des tournois enregistrés:\n")
        print(f"{'#':^4}{'Nom':^20}"
              f"{'Lieu':^20}{'Date de début':^14}{'Date de fin':^14}"
              f"{'Type':^14}")
        print("+" * 86)
        for i, tournament in enumerate(self.tournaments_list, start=1):
            print(f"{i:^4}{tournament['name'][:20]:^20}{tournament['place']:^20}"
                  f"{tournament['_start_date']:^14}{tournament['_end_date']:^14}"
                  f"{tournament['time_control']:^14}")

    def ask_user_choice(self):
        self.back_to_homepage()
        return HomePage()


class DisplayListRoundsByTournament(View):
    def show_menu(self):
        pass

    def ask_user_choice(self):
        print("Merci de saisir un numéro de tournoi:")
        tournament_id = int(input(">>> ") or 0)
        if tournament_id in tr.Tournament().list_of_ids:
            tournament_rounds = tr.DB.get_record_data("tournaments",
                                                           int(tournament_id),
                                                           "rounds")
            tournament_name = tr.DB.get_record_data("tournaments",
                                                        int(tournament_id),
                                                        "name",)
            if len(tournament_rounds) == 0:
                print("Aucun round pour le ", tournament_name,".",sep="")
            else:
                print("Voici la liste des rounds du tournoi:\n")
                print(f"{'Nom':^20}{'Date de début':^20}{'Heure de début':^20}{'Date de fin':^20}{'Heure de fin':^20}")
                print("+" * 100)
                for round in tournament_rounds:
                    print(f"{round['name'][:20]:^20}{round['_start_date']:^20}{round['_start_time']:^20}"
                          f"{round['_end_date']:^20}{round['_end_time']:^20}")
        self.back_to_homepage()
        return HomePage()


class DisplayListMatchesByTournament(View):
    def show_menu(self):
        print("Merci de saisir un numéro de tournoi:")
        tournament_id = int(input(">>> ") or 0)
        if tournament_id in tr.Tournament().list_of_ids:
            tournament = tr.Tournament().instantiate_from_db(tournament_id)
            if len(tournament.rounds) == 0 and not tournament.is_full():
                print(f"Aucun round n'existe pour ce tournoi.\n"
                      f"Merci de vérifier qu'il y a bien 8 joueurs inscrits à ce tournoi.")
            else:
                if tournament.nb_of_rounds == 0:
                    print("Aucun round n'existe pour ce tournoi.\n"
                          "Merci de vous assurer qu'il y a bien 8 joueurs inscrits.")
                else:
                    for i,round in enumerate(tournament.rounds,start=1):
                        print(round["name"])
                        print("+"*50)
                        for j,match in enumerate(round["matches"],start=1):
                            instantiated_match = mt.Match(match)
                            print(instantiated_match)
                        print("+" * 50)

    def ask_user_choice(self):
        self.back_to_homepage()
        return HomePage()


class DisplayListRankingsByTournament(View):
    def show_menu(self):
        print("Merci de saisir un numéro de tournoi:")
        tournament_id = int(input(">>> ") or 0)
        if tournament_id in tr.Tournament().list_of_ids:
            tournament = tr.Tournament().instantiate_from_db(tournament_id)
            if tournament.is_full():
                if tournament.is_finished:
                    statut = "définitif"
                else:
                    statut = "provisoire"
                print(f"Le classement {statut} du tournoi est le suivant:\n")
                print(f"{'Position':^10}{'Joueur':^20}{'Points':^20}")
                print("+"*50)
                for i,player in enumerate(tournament.tournament_ranking,start=1):
                    player_name = player["first_name"] + " " + player["family_name"]
                    print(f"{i:^10}{player_name:^20}{player['score']:^20}")
            else:
                print(f"Le tournoi n'a pas démarré, merci d'inscrire 8 joueurs au tournoi.")

    def ask_user_choice(self):
        self.back_to_homepage()
        return HomePage()


class ExportList(View):
    def show_menu(self):
        print("Cette fonctionnalité sera bientôt disponible.")
        # global LISTS_MENU
        # print("Choisissez une liste à exporter parmi les suivantes:")
        # self.menu = LISTS_MENU
        # for key in self.menu.items():
        #     print(key[0], ": ", key[1])
        # def export_list(filename, columns, data_list):
        #     with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        #         columns = columns
        #         writer = csv.DictWriter(csvfile, fieldnames=columns)
        #         writer.writeheader()
        #         writer.writerows(data_list)
        # Exemples:
        # export_list("Exportplayers.csv", list(pl.Player().__dict__.keys()), pl.PLAYERS_TABLE.all())
        # export_list("Exporttournaments.csv.", list(tr.Tournament().__dict__.keys()),
        #             tr.TOURNAMENTS_TABLE.all())

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
