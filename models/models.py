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
        DB.add_record("players",serialized_player)


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
        DB.add_record("tournaments",serialized_tournament)


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


def generate_round(tournament_id):
    global DB, TOURNAMENTS_TABLE
    tournament = DB.get_record_data("tournaments",tournament_id)
    rounds = tournament["rounds"]
    if len(rounds) == 0:
        new_round = Rounds("Round 1",TODAY,NOW)
        DB.update_record_data("tournaments","rounds",[new_round.__dict__],tournament_id)
    elif len(rounds) < int(tournament["nb_of_rounds"]):
        round_number = len(rounds) + 1
        new_round = Rounds("Round " + str(round_number),TODAY,NOW)
        DB.update_record_data("tournaments","rounds",[new_round.__dict__],tournament_id,True)
    else:
        print("Le tournoi a atteint son nombre maximal de rondes.")

def generate_matches(tournament_id, round_id):
    global DB, TOURNAMENTS_TABLE, PLAYERS_TABLE
    matches = []
    players = DB.get_record_data("tournaments",tournament_id,"players")
    nb_of_rounds = DB.get_record_data("tournaments",tournament_id,"nb_of_rounds")
    rounds = DB.get_record_data("tournaments", tournament_id, "rounds")
    if len(players) < 8:
        print(f"Il manque encore {8 - len(players)} joueurs pour que le tournoi soit complet.")
        return
    elif int(round_id) > int(nb_of_rounds):
        print(f"Il n'y a que {nb_of_rounds} tours dans ce tournoi.")
        return
    elif round_id == 1:
        sorted_players = sorted(players,key=lambda x:x["ranking"],reverse=False)
        for i in range(4):
            new_match = Matches(sorted_players[i]["first_name"] + " " +
                                   sorted_players[i]["family_name"],
                                   sorted_players[i+4]["first_name"] + " " +
                                   sorted_players[i+4]["family_name"])
            matches.append(new_match.pair)
        rounds[0]["matches"] = matches
        DB.update_record_data("tournaments","rounds",rounds,tournament_id)
        return
    # TODO Génération des matches pour les tours > tour n° 1

if __name__ == "__main__":
    pass
