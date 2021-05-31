#! /usr/bin/env python3
# coding: utf-8
from tinydb import TinyDB
from models import dbmanager
import time

TIME_CONTROL = {"1": "Bullet",
                "2": "Blitz",
                "3": "Coup rapide"}

POINTS = {"Match perdu":0,
          "Match nul":0.5,
          "Match gagné":1}

POINTS_LIST = list(POINTS.values())
DB = dbmanager.DBManager("db.json","tournaments","players")
TOURNAMENTS_TABLE = DB.tournaments
PLAYERS_TABLE = DB.players
TODAY = time.strftime("%d/%m/%Y")
NOW = time.strftime("%Hh%Mm%Ss")

class Players:
    """
            A class that represents a chess player.

            Attributes
            ----------
            first_name -> first_name of the player
            family_name -> family_name of the player
            birth_date -> date of birth of the player
            sex -> sex of the player
            ranking  -> ranking of the player

            Methods
            -------
            None
            """
    global DB, PLAYERS_TABLE
    def __init__(self, first_name="", family_name="", birth_date="", sex="", ranking="", add_to_db=False):
        serialized_player = {}
        self.first_name = first_name
        self.family_name = family_name
        self.birth_date = birth_date
        self.sex = sex
        self.ranking = ranking
        for attributes in self.__dict__.items():
            serialized_player[attributes[0]] = attributes[1]
        if add_to_db:
            DB.add_record("players",serialized_player)


class Tournaments:
    """
            A class that represents a tournament.

            Attributes
            ----------
            name -> name of the tournament
            place -> name of the place where the tournament takes place
            start_date -> start date of the tournament
            end_date -> end date of the tournament
            nb_of_rounds  -> number of rounds of the tournament (4 by default)
            rounds -> list of tournament's rounds
            players -> list of tournament's players
            time_control -> type of time control (Bullet, Blitz or Coup Rapide)
            description -> description of the tournament

            Methods
            -------
            generate_round -> generates a round instance inside
            the rounds parameter of a Tournament instance
            empty_tournament -> returns True if there are no
            players enlisted in the tournament, otherwise False
            full_tournament -> returns True if there are already
            8 players enlisted in the tournament, toherwise False
            """
    global TIME_CONTROL, DB, TOURNAMENTS_TABLE
    def __init__(self, name="", place="", start_date=TODAY, end_date=TODAY,
                 players=[],
                 time_control=TIME_CONTROL["1"], description="",
                 nb_of_rounds=4, add_to_db=False):
        players = []
        serialized_tournament = {}
        self.name = name
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.nb_of_rounds = nb_of_rounds
        self.rounds = []
        self.players = players
        self.time_control = time_control
        self.description = description
        for attributes in self.__dict__.items():
            serialized_tournament[attributes[0]] = attributes[1]
        if add_to_db:
            DB.add_record("tournaments",serialized_tournament)

    def empty_tournament(self):
        if len(self.players) == 0:
            return True
        else:
            return False

    def full_tournament(self):
        if len(self.players) == 8:
            return True
        else:
            return False

    def add_players(self,player):
        self.players.append(player.__dict__)

    def new_pair(self,player1,player2):
        rounds = self.rounds
        for round in rounds:
            for match in round["matches"]:
                if match[0][0] == player1 and match[1][0] == player2:
                    return False
                elif match[0][0] == player2 and match[1][0] == player1:
                    return False
        return True

    def tournament_ranking(self):
        pass

    def generate_round(self):
        rounds = self.rounds
        if len(rounds) < int(self.nb_of_rounds):
            round_number = len(rounds) + 1
            new_round = Rounds("Round " + str(round_number), TODAY, NOW)
            self.rounds.append(new_round.__dict__)
        else:
            print("Le tournoi a atteint son nombre maximal de rondes.")

    def generate_matches(self,round_id):
        matches = []
        players = self.players
        nb_of_rounds = self.nb_of_rounds
        rounds = self.rounds
        if len(players) < 8:
            print(f"Il manque encore {8 - len(players)} joueurs pour que le tournoi soit complet.")
            return
        elif int(round_id) > int(nb_of_rounds):
            print(f"Il n'y a que {nb_of_rounds} tours dans ce tournoi.")
            return
        elif int(round_id) == 1:
            sorted_players = sorted(players, key=lambda x: x["ranking"], reverse=False)
            for i in range(4):
                new_match = Matches(sorted_players[i]["first_name"] + " " +
                                           sorted_players[i]["family_name"],
                                           sorted_players[i + 4]["first_name"] + " " +
                                           sorted_players[i + 4]["family_name"])
                matches.append(new_match.pair)
            rounds[0]["matches"] = matches
            return
        # TODO Génération des matches pour les tours > tour n° 1


class Rounds:
    """
            A class that represents a tournament's round.

            Attributes
            ----------
            name -> name of the tournament's round
            start_date -> start date of the tournament's round
            start_time -> start time of the tournament's round
            end_date -> end date of the tournament's round
            end_time -> end time of the tournament's round
            matches -> list of matches of the tournament's round

            Methods
            -------
            round_played -> returns True if the round is over (i.e.
            all round's matches have been played) or False if not
            """
    def __init__(self, name, start_date, start_time):
        self.name = name
        self.start_date = start_date
        self.start_time = start_time
        self.end_date = ""
        self.end_time = ""
        self.matches = []

    def round_played(self):
        for match in self.matches:
            if match.match_played is False:
                return False
            return True

class Matches:
    """
            A class that represents a round's round.

            Attributes
            ----------
            player1 -> player data for the first player of the match
            player2 -> player data for the second player of the match
            pair -> a list of two tuples, each tuple representing a player
            and its score

            Methods
            -------
            match_played -> returns True if the match is over (i.e.
            sum of points of both players is greater than 0) or False if not
            match_score -> updates the score of the match
            """
    def __init__(self,player1,player2):
        self.player1 = player1
        self.player2 = player2
        self.pair = [(player1,0),(player2,0)]

    def match_played(self):
        somme = self.pair[0][1] + self.pair[1][1]
        if somme > 0:
            return True
        else:
            return False

    def match_score(self,score_player1,score_player2):
        self.pair = [(self.player1,score_player1),(self.player2,score_player2)]
        return

if __name__ == "__main__":
    pass
