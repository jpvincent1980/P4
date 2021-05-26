#! /usr/bin/env python3
# coding: utf-8
from tinydb import TinyDB,Query

TIME_CONTROL = {"1": "Bullet",
                "2": "Blitz",
                "3": "Coup rapide"}

DB = TinyDB("db.json")
TOURNAMENTS_TABLE = DB.table("tournaments")
PLAYERS_TABLE = DB.table("players")

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
    def __init__(self, name="", place="", start_date="", end_date="",
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
        self.rounds = ["Round 1"]
        self.players = players
        self.time_control = time_control
        self.description = description
        for attributes in self.__dict__.items():
            serialized_tournament[attributes[0]] = attributes[1]
        TOURNAMENTS_TABLE.insert(serialized_tournament)

    def pairing(self, round_number):
        # Si premier tour, triez les joueurs en fonction de leur classement
        # puis séparez les joueurs en deux moitiés, les meilleurs joueurs
        # des deux moitiés s'affrontent, etc.
        # Pour les tours suivants, triez les joueurs en fonction de leur
        # nombre total de points et en cas d'égalité,
        # en fonction de leur classement, et associez les joueurs 1 et 2, 3
        # et 4, ect. Si des joueurs se sont déjà
        # affrontés lors d'un même tour, faites jouer le meilleur joueur
        # contre celui classé après.
        pass


class Rounds:
    def __init__(self, name, start_date, start_time, end_date, end_time):
        self.name = name
        self.start_date = start_date
        self.start_time = start_time
        self.end_date = end_date
        self.end_time = end_time
        self.matches = []


class Matches:
    def __init__(self):
        self.players_pair = ()
        self.players_color = ()


def add_players(tournament_id,player_id):
    serialized_player = PLAYERS_TABLE.get(doc_id=player_id)
    serialized_player.update({"id": player_id})
    current_tournament_players = TOURNAMENTS_TABLE.get(doc_id=tournament_id)["players"]
    current_tournament_players.append(serialized_player)
    TOURNAMENTS_TABLE.update({"players":current_tournament_players},doc_ids=[tournament_id])
    return

if __name__ == "__main__":
    pass
