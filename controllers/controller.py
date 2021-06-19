#! /usr/bin/env python3
# coding: utf-8
import csv
import views.views
from views import views
from models import player as pl
from models import tournament as tr
from models import round as rn
from models import match as mt

MAIN_MENU = {"1": "Créer un nouveau tournoi",
             "2": "Créer un nouveau joueur",
             "3": "Inscrire un joueur à un tournoi",
             "4": "Entrer les résultats d'un match",
             "5": "Entrer le classement d'un joueur",
             "6": "Afficher une liste",
             "7": "Exporter une liste",
             "9": "Quitter le programme"}

MAIN_MENU_COMMAND = {"1": views.CreateTournamentView(),
             "2": views.CreatePlayerView(),
             "3": views.AddPlayerToTournamentView(),
             "4": views.EnterMatchScoreView(),
             "5": views.EnterPlayerRankingView(),
             "6": views.DisplayList(),
             "7": views.ExportList(),
             "9": views.EndPage()}

LISTS_MENU = {"1": "Liste de tous les joueurs",
              "2": "Liste de tous les joueurs d'un tournoi",
              "3": "Liste de tous les tournois",
              "4": "Liste de tous les tours d'un tournoi",
              "5": "Liste de tous les matchs d'un tournoi",
              "6": "Classement d'un tournoi",
              "8": "Retour au menu principal",
              "9": "Quitter le programme"}

LISTS_MENU_COMMAND = {"1": views.DisplayListPlayers(),
              "2": views.DisplayListPlayersByTournament(),
              "3": views.DisplayListTournaments(),
              "4": views.DisplayListRoundsByTournament(),
              "5": views.DisplayListMatchesByTournament(),
              "6": views.DisplayListRankingsByTournament(),
              "8": views.HomePage(),
              "9": views.EndPage()}

SORTING_MENU = {"1": "Ordre alphabétique",
                "2": "Classement"}

VIEWS_REQUIRING_TOURNAMENT = (views.AddPlayerToTournamentView,
                              views.EnterMatchScoreView,
                              views.DisplayListPlayersByTournament,
                              views.DisplayListTournaments,
                              views.DisplayListRoundsByTournament,
                              views.DisplayListMatchesByTournament,
                              views.DisplayListRankingsByTournament)

VIEWS_REQUIRING_PLAYER = (views.AddPlayerToTournamentView,
                          views.EnterPlayerRankingView,
                          views.DisplayListPlayers,
                          views.DisplayListPlayersByTournament)

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
        self.model = pl.Player
        self.view = views.HomePage()
        self.export = False

    def entry_controller(self,user_choice):
        if isinstance(user_choice,views.View):
            return True
        else:
            if type(user_choice) == tuple:
                for element in user_choice:
                    for character in element:
                        if character == "" \
                                or ord(character) < 48 \
                                or ord(character) > 57:
                            return False
                        else:
                            return True
            else:
                for character in user_choice:
                    if character == "" \
                        or ord(character) < 48 \
                            or ord(character) > 57:
                        return False
                    else:
                        return True

    def menu_controller(self,user_choice):
        if user_choice not in self.view.menu:
            views.InvalidChoiceView().show_menu()
            return self.view
        elif self.view.menu == MAIN_MENU:
            return MAIN_MENU_COMMAND[user_choice]
        elif self.view.menu == LISTS_MENU:
            return LISTS_MENU_COMMAND[user_choice]

    def check_if_any_player(self):
        if len(pl.PLAYERS_TABLE) > 0:
            return True
        else:
            return False

    def player_exists(self,player_id):
        if player_id in pl.Player.list_of_ids():
            return True
        else:
            return False

    def check_if_any_tournament(self):
        if len(tr.TOURNAMENTS_TABLE) > 0:
            return True
        else:
            return False

    def tournament_exists(self,tournament_id):
        if tournament_id in tr.Tournament.list_of_ids():
            return True
        else:
            return False

    def check_tournament_status(self,tournament):
        if tournament.tournament_nb_of_rounds < tournament.nb_of_rounds:
            if len(tournament.players) >= 8 and \
                    len(tournament.tournament_unfinished_rounds_ids) == 0:
                tournament.generate_round()
                tournament.generate_matches()
                tr.DB.update_record_data("tournaments",
                                         tournament._id,
                                         "rounds",
                                         tournament.rounds)
                return "NewRoundGenerated"
        elif tournament.tournament_nb_of_rounds == tournament.nb_of_rounds:
            if len(tournament.tournament_unfinished_rounds_ids) == 0:
                tournament._end_date = tr.TODAY
                tr.DB.update_record_data("tournaments",
                                         tournament._id,
                                         "_end_date",
                                         tournament._end_date)
                return "TournamentIsOver"

    def uncompleted_rounds(self,tournament):
        rounds_list = []
        for round in tournament.rounds:
            if not round.round_completed:
                rounds_list.append(round)
        return rounds_list


    def check_players(self):
        if self.tournament.tournament_nb_of_players == 0:
            print("Aucun joueur n'est inscrit au", self.tournament.name, "pour le moment.")
        elif self.tournament.tournament_nb_of_players > 0:
            if self.tournament.tournament_nb_of_players >= 8:
                print("Le tournoi est complet.")
            print("Voici la liste des joueurs déjà inscrits au", self.tournament.name, ":")
            for player in self.tournament.players:
                print(player["id"], "->", player["first_name"], player["family_name"])
                self.tournament.tournament_players_ids.append(player["id"])
        return

    def round_controller(self,round_id):
        pass

    def match_controller(self,match_id):
        pass

    def export_list(self, data_list, filename="export.csv"):
        with open(filename, "w", newline="", encoding="utf-8") as csv_file:
            columns = [key for key in data_list[0]]
            writer = csv.DictWriter(csv_file, fieldnames=columns)
            writer.writeheader()
            writer.writerows(data_list)

    def start(self):
        self.start = True
        counter = 0
        while self.start:
            if counter == 0:
                self.view.show_title()
            counter += 1
            if isinstance(self.view, VIEWS_REQUIRING_TOURNAMENT):
                if not self.check_if_any_tournament():
                    self.view = views.NoTournament()
            if isinstance(self.view, VIEWS_REQUIRING_PLAYER):
                if not self.check_if_any_player():
                    self.view = views.NoPlayer()
            if isinstance(self.view, views.EnterMatchScoreView):
                if len(tr.Tournament.uncompleted_tournaments()) == 0:
                    self.view = views.NoOpenTournament()
                else:
                    self.view = views.EnterMatchScoreView(tr.Tournament.uncompleted_tournaments())
            self.view.show_menu()
            user_choice = self.view.ask_user_choice()
            if not self.entry_controller(user_choice):
                views.InvalidChoiceView().show_menu()
                next_view = self.view
            else:
                if isinstance(self.view,views.HomePage):
                    next_view = self.menu_controller(user_choice)
                elif isinstance(self.view,views.CreateTournamentView):
                    new_tournament = tr.Tournament(name=self.view.name,
                                                   place=self.view.place,
                                                   start_date=tr.TODAY,
                                                   end_date="",
                                                   time_control=tr.TIME_CONTROL[self.view.time_control],
                                                   description=self.view.description,
                                                   add_to_db=True)
                    new_tournament_name = new_tournament.name
                    tr.Tournament.update_ids()
                    next_view = views.TournamentCreationValidationView(new_tournament_name)
                elif isinstance(self.view,views.CreatePlayerView):
                    new_player = pl.Player(first_name=self.view.first_name,
                                           family_name=self.view.family_name,
                                           birth_date=self.view.birth_date,
                                           sex=self.view.sex,
                                           ranking=self.view.ranking,
                                           add_to_db=True)
                    pl.Player.update_ids()
                    next_view = views.PlayerCreationValidationView(new_player)
                elif isinstance(self.view, views.AddPlayerToTournamentView):
                    if not self.tournament_exists(int(user_choice)):
                        views.UnknownTournament().show_menu()
                        next_view = self.view
                    else:
                        tournament_id = user_choice
                        tournament = tr.Tournament.instantiate_from_db(int(tournament_id))
                        available_players_ids = tournament.available_players_ids
                        next_view = views.DisplayAvailablePlayers(available_players_ids)
                elif isinstance(self.view, views.DisplayAvailablePlayers):
                    if not self.player_exists(int(user_choice)):
                        views.UnknownPlayer().show_menu()
                        next_view = self.view
                    elif int(user_choice) in tournament.tournament_players_ids:
                        views.PlayerAlreadyEnlisted().show_menu()
                        next_view = self.view
                    else:
                        player_id = user_choice
                        new_player = pl.Player.instantiate_from_db(int(player_id))
                        new_player_full_name = new_player.first_name + " " + new_player.family_name
                        new_player = new_player.__dict__
                        tr.DB.update_record_data("tournaments",int(tournament_id),"players",new_player,True)
                        tournament = tr.Tournament.instantiate_from_db(int(tournament_id))
                        completed = False
                        status = self.check_tournament_status(tournament)
                        if status == "NewRoundGenerated":
                            completed = True
                        tournament_name = tournament.name
                        next_view = views.AddPlayerValidationView(new_player_full_name,tournament_name,completed)
                elif isinstance(self.view, views.EnterMatchScoreView):
                    if not self.tournament_exists(int(user_choice)):
                        views.UnknownTournament().show_menu()
                        next_view = self.view
                    elif int(user_choice) not in tr.Tournament.uncompleted_tournaments_ids():
                        next_view = views.InactiveTournament()
                    else:
                        tournament_id = user_choice
                        tournament = tr.Tournament.instantiate_from_db(int(tournament_id))
                        rounds_list = []
                        for round in tournament.rounds:
                            round = rn.Round.instantiate_from_serialized_round(round)
                            if not round.round_completed:
                                rounds_list.append(round)
                        next_view = views.DisplayAvailableRounds(rounds_list)
                elif isinstance(self.view, views.DisplayAvailableRounds):
                    round_id = int(user_choice)
                    if round_id not in tournament.tournament_rounds_ids:
                        views.UnknownRound().show_menu()
                        next_view = self.view
                    elif round_id not in tournament.tournament_unfinished_rounds_ids:
                        views.CompletedRound().show_menu()
                        next_view = self.view
                    else:
                        matches_list = []
                        round = rn.Round.instantiate_from_serialized_round(tournament.rounds[round_id - 1])
                        for i,match in enumerate(round.matches,start=1):
                            player1 = pl.Player.instantiate_from_serialized_player(match[0][0])
                            player2 = pl.Player.instantiate_from_serialized_player(match[1][0])
                            score_player1 = match[0][1]
                            score_player2 = match[1][1]
                            match = mt.Match(player1, player2, score_player1, score_player2)
                            if not match.match_completed():
                                matches_list.append((i,match))
                        next_view = views.DisplayAvailableMatches(matches_list)
                elif isinstance(self.view, views.DisplayAvailableMatches):
                    match_id = int(user_choice)
                    if match_id not in round.list_of_unplayed_matches_ids:
                        views.UnknownMatch().show_menu()
                        next_view = self.view
                    else:
                        player1 = pl.Player.instantiate_from_serialized_player(tournament.rounds[round_id-1]["matches"][match_id-1][0][0])
                        player2 = pl.Player.instantiate_from_serialized_player(tournament.rounds[round_id-1]["matches"][match_id-1][1][0])
                        score_player1 = tournament.rounds[round_id-1]["matches"][match_id-1][0][1]
                        score_player2 = tournament.rounds[round_id-1]["matches"][match_id-1][1][1]
                        instantiated_match = mt.Match(player1, player2, score_player1, score_player2)
                        next_view = views.EnterMatchScoresView(instantiated_match,
                                                               player1,
                                                               player2)
                elif isinstance(self.view, views.EnterMatchScoresView):
                    score_player1 = float(user_choice[0])
                    score_player2 = float(user_choice[1])
                    round_completed = False
                    if (score_player1 and score_player2) in mt.POINTS_LIST and \
                            score_player1 + score_player2 == 1:
                        instantiated_match.match_score(score_player1, score_player2)
                        tournament.rounds[round_id - 1]["matches"][match_id - 1] = instantiated_match.pair
                        tr.DB.update_record_data("tournaments",
                                                 (int(tournament_id)),
                                                 "rounds",
                                                 tournament.rounds)
                        updated_tournament = tr.Tournament.instantiate_from_db(int(tournament_id))
                        tournament_completed = updated_tournament.tournament_completed
                        updated_round = rn.Round.instantiate_from_serialized_round(updated_tournament.rounds[round_id - 1])
                        if updated_round.round_completed:
                            updated_tournament.rounds[round_id - 1]["_end_date"] = tr.TODAY
                            updated_tournament.rounds[round_id - 1]["_end_time"] = tr.NOW
                            tr.DB.update_record_data("tournaments",
                                                     (int(tournament_id)),
                                                     "rounds",
                                                     updated_tournament.rounds)
                            round_completed = True
                        self.check_tournament_status(updated_tournament)
                        next_view = views.EnterMatchScoresValidationView(round_completed,
                                                                         tournament_completed)
                    else:
                        views.IncorrectScoresView().show_menu()
                        next_view = self.view
                elif isinstance(self.view, views.EnterPlayerRankingView):
                    if not self.player_exists(int(user_choice)):
                        next_view = views.UnknownPlayer()
                    else:
                        player_id = int(user_choice)
                        player_full_name = ""
                        old_ranking = ""
                        for player in pl.PLAYERS_TABLE:
                            if player["_id"] == player_id:
                                player_full_name = player["first_name"] + \
                                                        " " + \
                                                        player["family_name"]
                                old_ranking = player["_ranking"]
                        next_view = views.EnterNewRankingView(player_full_name, old_ranking)
                elif isinstance(self.view, views.EnterNewRankingView):
                    pl.DB.update_record_data("players",player_id,"_ranking",self.view.new_ranking)
                    next_view = views.HomePage()
                elif isinstance(self.view,views.DisplayList):
                    next_view = self.menu_controller(user_choice)
                elif isinstance(self.view,views.DisplayListPlayers):
                    sorting_choice = user_choice
                    players_list = pl.Player.players_list(sorting_choice)
                    if not self.export:
                        next_view = views.DisplayListPlayersResults(players_list)
                    else:
                        self.export_list(players_list)
                        self.export = False
                        next_view = views.ExportListValidation()
                elif isinstance(self.view,views.DisplayListPlayersByTournament):
                    tournament_id = user_choice
                    if not self.tournament_exists(int(tournament_id)):
                        views.UnknownTournament().show_menu()
                        next_view = self.view
                    else:
                        tournament = tr.Tournament.instantiate_from_db(int(tournament_id))
                        if len(tournament.players) < 1:
                            next_view = views.NoPlayersEnlistedView()
                        else:
                            views.DisplayListPlayers().show_menu()
                            sorting_choice = views.DisplayListPlayers().ask_user_choice()
                            players_list = []
                            if sorting_choice == "1":
                                for player in sorted(tournament.players, key=lambda x: x['family_name']):
                                    players_list.append(player)
                            elif sorting_choice == "2":
                                for player in sorted(tournament.players, key=lambda x: int(x['_ranking'])):
                                    players_list.append(player)
                            if not self.export:
                                next_view = views.DisplayListPlayersByTournamentResults(players_list)
                            else:
                                self.export_list(players_list)
                                self.export = False
                                next_view = views.ExportListValidation()
                elif isinstance(self.view,views.DisplayListTournaments):
                    tournaments_list = tr.Tournament.tournaments_list()
                    if not self.export:
                        next_view = views.DisplayListTournamentsResults(tournaments_list)
                    else:
                        self.export_list(tournaments_list)
                        self.export = False
                        next_view = views.ExportListValidation()
                elif isinstance(self.view, views.DisplayListRoundsByTournament):
                    tournament_id = user_choice
                    if not self.tournament_exists(int(tournament_id)):
                        views.UnknownTournament().show_menu()
                        next_view = self.view
                    else:
                        tournament = tr.Tournament.instantiate_from_db(int(tournament_id))
                        tournament_name = tournament.name
                        rounds_list = tournament.rounds
                        if len(rounds_list) == 0:
                            next_view = views.NoRound()
                        else:
                            if not self.export:
                                next_view = views.DisplayListRoundsByTournamentResults(rounds_list,
                                                                                       tournament_name)
                            else:
                                self.export_list(rounds_list)
                                self.export = False
                                next_view = views.ExportListValidation()
                elif isinstance(self.view, views.DisplayListMatchesByTournament):
                    tournament_id = user_choice
                    if not self.tournament_exists(int(tournament_id)):
                        views.UnknownTournament().show_menu()
                        next_view = self.view
                    else:
                        tournament = tr.Tournament.instantiate_from_db(int(tournament_id))
                        tournament_name = tournament.name
                        rounds_list = tournament.rounds
                        if len(rounds_list) == 0:
                            next_view = views.NoRound()
                        else:
                            matches_list = []
                            for i, round in enumerate(rounds_list, start=1):
                                for j,match in enumerate(round["matches"],start=1):
                                    player1 = pl.Player.instantiate_from_serialized_player(match[0][0])
                                    player2 = pl.Player.instantiate_from_serialized_player(match[1][0])
                                    score_player1 = match[0][1]
                                    score_player2 = match[1][1]
                                    instantiated_match = mt.Match(player1, player2, score_player1, score_player2)
                                    matches_list.append((round["name"],instantiated_match))
                                if not self.export:
                                    next_view = views.DisplayListMatchesByTournamentResults(matches_list,
                                                                                            tournament_name)
                                else:
                                    #TODO Gérer l'export des matches (pb de tuple)
                                    self.export_list(matches_list)
                                    self.export = False
                                    next_view = views.ExportListValidation()
                elif isinstance(self.view, views.DisplayListRankingsByTournament):
                    tournament_id = user_choice
                    if not self.tournament_exists(int(tournament_id)):
                        views.UnknownTournament().show_menu()
                        next_view = self.view
                    else:
                        tournament = tr.Tournament.instantiate_from_db(int(tournament_id))
                        tournament_name = tournament.name
                        rankings_list = tournament.tournament_ranking
                        status = "provisoire"
                        if tournament.tournament_completed and tournament.is_full():
                            status = "définitif"
                        if len(tournament.players) == 0:
                            next_view = views.NoPlayersEnlistedView()
                        else:
                            if not self.export:
                                next_view = views.DisplayListRankingsByTournamentResults(rankings_list,
                                                                                         tournament_name,
                                                                                         status)
                            else:
                                self.export_list(rankings_list)
                                self.export = False
                                next_view = views.ExportListValidation()
                elif isinstance(self.view, views.ExportList):
                    self.export = True
                    next_view = views.DisplayList()
                else:
                    next_view = views.HomePage()
                self.view = next_view

if __name__ == "__main__":
    pass
