#! /usr/bin/env python3
# coding: utf-8
from views import views
from models import player as pl
from models import tournament as tr

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

    def menu_controller(self,user_choice):
        if user_choice not in self.view.menu:
            print("Choix non valide. Veuillez ressaisir un choix "
                  "parmi la liste.")
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
                print("Un nouveau round vient d'être généré pour ce tournoi.")
        elif tournament.tournament_nb_of_rounds == tournament.nb_of_rounds:
            if len(tournament.tournament_unfinished_rounds_ids) == 0:
                tournament._end_date = tr.TODAY
                tr.DB.update_record_data("tournaments",
                                         tournament._id,
                                         "_end_date",
                                         tournament._end_date)

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
            self.view.show_menu()
            user_choice = self.view.ask_user_choice()
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
                new_player_name = new_player.first_name + " " + new_player.family_name
                pl.Player.update_ids()
                next_view = views.PlayerCreationValidationView(new_player_name)
            elif isinstance(self.view, views.AddPlayerToTournamentView):
                if not self.tournament_exists(user_choice):
                    next_view = views.UnknownTournament()
                else:
                    tournament_id = user_choice
                    tournament = tr.Tournament.instantiate_from_db(int(tournament_id))
                    available_players_ids = tournament.available_players_ids
                    next_view = views.DisplayAvailablePlayers(available_players_ids)
            elif isinstance(self.view, views.DisplayAvailablePlayers):
                player_id = user_choice
                new_player = pl.Player.instantiate_from_db(player_id)
                new_player_full_name = new_player.first_name + " " + new_player.family_name
                new_player = new_player.__dict__
                tr.DB.update_record_data("tournaments",tournament_id,"players",new_player,True)
                tournament = tr.Tournament.instantiate_from_db(tournament_id)
                self.check_tournament_status(tournament)
                tournament_name = tournament.name
                next_view = views.AddPlayerValidationView(new_player_full_name,tournament_name)
            elif isinstance(self.view, views.EnterMatchScoreView):
                if not self.tournament_exists(user_choice):
                    next_view = views.UnknownTournament()
                else:
                    tournament_id = user_choice
                    tournament = tr.Tournament.instantiate_from_db(int(tournament_id))
                    next_view = views.DisplayAvailableRounds(tournament)
            elif isinstance(self.view, views.DisplayAvailableRounds):
                round_id = user_choice
                next_view = views.DisplayAvailableMatches(tournament, round_id)
            elif isinstance(self.view, views.DisplayAvailableMatches):
                match_id = user_choice
                next_view = views.EnterMatchScoresView(tournament, round_id, match_id)
            elif isinstance(self.view, views.EnterMatchScoresView):
                next_view = views.HomePage()
            elif isinstance(self.view, views.EnterPlayerRankingView):
                if not self.player_exists(user_choice):
                    next_view = views.UnknownPlayer()
                else:
                    player_id = user_choice
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
                next_view = views.DisplayListPlayersResults(players_list)
            elif isinstance(self.view,views.DisplayListTournaments):
                tournaments_list = tr.Tournament.tournaments_list()
                next_view = views.DisplayListTournamentsResults(tournaments_list)
            else:
                next_view = views.HomePage()
            self.view = next_view

if __name__ == "__main__":
    pass
