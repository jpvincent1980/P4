#! /usr/bin/env python3
# coding: utf-8
from tinydb import TinyDB,Query
import time

TIME_CONTROL = {"1": "Bullet",
                "2": "Blitz",
                "3": "Coup rapide"}

POINTS = {"Match perdu":0,
          "Match nul":0.5,
          "Match gagné":1}

POINTS_LIST = list(POINTS.values())
DB = TinyDB("db.json")
TOURNAMENTS_TABLE = DB.table("tournaments")
PLAYERS_TABLE = DB.table("players")
TODAY = time.strftime("%d/%m/%Y")
NOW = time.strftime("%Hh%Mm%Ss")

class Players:
    global DB, PLAYERS_TABLE
    def __init__(self, first_name, family_name, birth_date, sex, ranking):
        serialized_player = {}
        self.first_name = first_name
        self.family_name = family_name
        self.birth_date = birth_date
        self.sex = sex
        self.ranking = ranking
        for attributes in self.__dict__.items():
            serialized_player[attributes[0]] = attributes[1]
        PLAYERS_TABLE.insert(serialized_player)


class Tournaments:
    global TIME_CONTROL, DB, TOURNAMENTS_TABLE
    def __init__(self, name="", place="", start_date=TODAY, end_date=TODAY,
                 players=[],
                 time_control=TIME_CONTROL["1"], description="",
                 nb_of_rounds=4):
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
        TOURNAMENTS_TABLE.insert(serialized_tournament)


class Rounds:
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


def add_players(tournament_id, player_id):
    serialized_player = PLAYERS_TABLE.get(doc_id=player_id)
    serialized_player.update({"id": player_id})
    current_tournament_players = TOURNAMENTS_TABLE.get(doc_id=tournament_id)["players"]
    current_tournament_players.append(serialized_player)
    TOURNAMENTS_TABLE.update({"players":current_tournament_players},doc_ids=[tournament_id])
    return

def update_player_ranking(player_id, new_ranking):
    PLAYERS_TABLE.update({"ranking": new_ranking},doc_ids=[player_id])

def generate_round(tournament_id):
    global DB, TOURNAMENTS_TABLE
    tournament = TOURNAMENTS_TABLE.get(doc_id=int(tournament_id))
    rounds = tournament["rounds"]
    if len(rounds) == 0:
        new_round = Rounds("Round 1", TODAY, NOW)
        TOURNAMENTS_TABLE.update({"rounds":[new_round.__dict__]},doc_ids=[tournament_id])
    elif len(rounds) < int(tournament["nb_of_rounds"]):
        round_number = len(rounds) + 1
        new_round = Rounds("Round " + str(round_number), TODAY, NOW)
        rounds.append(new_round.__dict__)
        TOURNAMENTS_TABLE.update({"rounds": rounds}, doc_ids=[tournament_id])
    else:
        print("Le tournoi a atteint son nombre maximal de rondes.")

if __name__ == "__main__":
    match = Matches("Joueur 1","Joueur 2")
    print(match.match_played())
    match.match_score(0,1)
    print(match.pair)
    print(match.match_played())
    print(match.pair)
