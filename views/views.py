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


class NoPlayersEnlistedView(View):
    def show_menu(self):
        print("Aucun joueur n'est inscrit à ce tournoi.")

    def ask_user_choice(self):
        self.back_to_homepage()
        return HomePage()


class UncorrectScoresView(View):
    def show_menu(self):
        print(f"La somme des points attribués doit être égale à 1.\n"
              f"Les points attribuables ne peuvent être que: "
              f"{mt.POINTS_LIST}")

    def ask_user_choice(self):
        self.back_to_homepage()
        return HomePage()


class InvalidChoiceView(View):
    def show_menu(self):
        print("Choix non valide.")

    def ask_user_choice(self):
        self.back_to_homepage()
        return HomePage()


class NoRound(View):
    def show_menu(self):
        print(f"Aucun round n'existe pour ce tournoi.\n"
              f"Vérifiez le nombre de joueurs inscrits.")

    def ask_user_choice(self):
        self.back_to_homepage()


class NoMatch(View):
    def show_menu(self):
        print(f"Aucun match n'existe pour ce tournoi.\n"
              f"Vérifiez le nombre de joueurs inscrits.")

    def ask_user_choice(self):
        self.back_to_homepage()


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
    def __init__(self,player_full_name,tournament_name,completed=False):
        self.player_full_name = player_full_name
        self.tournament_name = tournament_name
        self.completed = completed

    def show_menu(self):
        print(f"{self.player_full_name} a bien été inscrit au {self.tournament_name}.")
        if self.completed:
            print(f"Un round vient d'être généré pour ce tournoi.")

    def ask_user_choice(self):
        self.back_to_homepage()
        return HomePage()


class EnterMatchScoreView(View):
    def show_menu(self):
        print(f"Choisissez un tournoi parmi les suivants:")
        for tournament in tr.Tournament.full_tournaments():
            print(f"{tournament['_id']} -> {tournament['name']}")

    def ask_user_choice(self):
        tournament_id = int(input(">>> ") or 0)
        return tournament_id


class DisplayAvailableRounds(View):
    def __init__(self,tournament):
        self.tournament = tournament

    def show_menu(self):
        print(f"Choisissez un round parmi les suivants:")
        for round in self.tournament.rounds:
            print(f"{round['name'][-1]} -> {round['name']}")

    def ask_user_choice(self):
        round_id = int(input(">>> ") or 0)
        return round_id

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
        match_id = int(input(">>> ") or 0)
        return match_id

class EnterMatchScoresView(View):
    def __init__(self, match, player1_full_name, player2_full_name):
        self.match = match
        self.player1_full_name = player1_full_name
        self.player2_full_name = player2_full_name

    def show_menu(self):
        print(f"Entrez les scores du match {self.player1_full_name} vs "
              f"{self.player2_full_name}:")

    def ask_user_choice(self):
        score_player1 = input(f">>> Score de {self.player1_full_name}:\n")
        score_player2 = input(f">>> Score de {self.player2_full_name}:\n")
        return score_player1, score_player2


class EnterMatchScoresValidationView(View):
    def __init__(self, round_completed, tournament_completed):
        self.round_completed = round_completed
        self.tournament_completed = tournament_completed

    def show_menu(self):
        print(f"Le résultat du match a bien été mis à jour.")
        if self.round_completed:
            print(f"Le round est terminé.")
            if self.tournament_completed:
                print(f"Il s'agissait du dernier round, le tournoi est à présent terminé.")
            else:
                print(f"Un nouveau round a été généré.")

    def ask_user_choice(self):
        self.back_to_homepage()
        return HomePage()


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
        print(f"Choisissez un tournoi parmi les suivants:")
        for id,tournament in enumerate(tr.TOURNAMENTS_TABLE,start=1):
            print(f"{id} -> {tournament['name']}")

    def ask_user_choice(self):
        tournament_id = int(input(">>> ") or 0)
        return tournament_id


class DisplayListPlayersByTournamentResults(View):
    def __init__(self,players_list):
        self.players_list = players_list

    def show_menu(self):
        print(f"Voici la liste des joueurs inscrits à ce tournoi:\n")
        print(f"{'#':^4}{'Prénom':^20}{'Nom':^20}{'Date de Naissance':^20}{'H/F':^6}{'Classement':^10}")
        print("+" * 80)
        for i,player in enumerate(self.players_list,start=1):
            print(f"{i:^4}{player['first_name']:^20}{player['family_name']:^20}"
                  f"{player['_birth_date']:^20}{player['_sex']:^6}{player['_ranking']:^10}")
        return

    def ask_user_choice(self):
        self.back_to_homepage()
        return HomePage()


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
        print(f"Choisissez un tournoi parmi les suivants:")
        for id,tournament in enumerate(tr.TOURNAMENTS_TABLE,start=1):
            print(f"{id} -> {tournament['name']}")

    def ask_user_choice(self):
        tournament_id = int(input(">>> ") or 0)
        return tournament_id

class DisplayListRoundsByTournamentResults(View):
    def __init__(self, rounds_list, tournament_name):
        self.rounds_list = rounds_list
        self.tournament_name = tournament_name

    def show_menu(self):
        print(f"Voici la liste des rounds du {self.tournament_name}:\n")
        print(f"{'Nom':^20}{'Date de début':^20}{'Heure de début':^20}{'Date de fin':^20}{'Heure de fin':^20}")
        print("+" * 100)
        for round in self.rounds_list:
            print(f"{round['name'][:20]:^20}{round['_start_date']:^20}{round['_start_time']:^20}"
                  f"{round['_end_date']:^20}{round['_end_time']:^20}")
        return

    def ask_user_choice(self):
        self.back_to_homepage()
        return HomePage()


class DisplayListMatchesByTournament(View):
    def show_menu(self):
        print(f"Choisissez un tournoi parmi les suivants:")
        for id,tournament in enumerate(tr.TOURNAMENTS_TABLE,start=1):
            print(f"{id} -> {tournament['name']}")

    def ask_user_choice(self):
        tournament_id = int(input(">>> ") or 0)
        return tournament_id


class DisplayListMatchesByTournamentResults(View):
    def __init__(self,matches_list,tournament_name):
        self.matches_list = matches_list
        self.tournament_name = tournament_name

    def show_menu(self):
        print(f"Voici la liste des matchs du {self.tournament_name}:\n")
        for round, match in self.matches_list:
            print(f"{round} \n ********** \n {match} \n")

    def ask_user_choice(self):
        self.back_to_homepage()
        return HomePage()


class DisplayListRankingsByTournament(View):
    def show_menu(self):
        print(f"Choisissez un tournoi parmi les suivants:")
        for id,tournament in enumerate(tr.TOURNAMENTS_TABLE,start=1):
            print(f"{id} -> {tournament['name']}")

    def ask_user_choice(self):
        tournament_id = int(input(">>> ") or 0)
        return tournament_id


class DisplayListRankingsByTournamentResults(View):
    def __init__(self,rankings_list,status):
        self.rankings_list = rankings_list
        self.status = status

    def show_menu(self):
        print(f"Le classement {self.status} du tournoi est le suivant:\n")
        print(f"{'Position':^10}{'Prénom':^20}{'Nom':^20}{'Points':^20}")
        print("+" * 70)
        for i, player in enumerate(self.rankings_list, start=1):
            print(f"{i:^10}{player['first_name']:^20}{player['family_name']:^20}{player['score']:^20}")


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
