#! /usr/bin/env python3
# coding: utf-8

class Players:

    all_players = []
    def __init__(self,first_name,family_name,birth_date,sex,ranking):
        self.first_name = first_name
        self.family_name = family_name
        self.birth_date = birth_date
        self.sex = sex
        self.ranking = ranking
        Players.all_players.append(self)


TIME_CONTROL = {"1":"Bullet",
                "2":"Blitz",
                "3":"Coup rapide"}

class Tournaments:

    all_tournaments = []
    global TIME_CONTROL
    def __init__(self,name="",place="",start_date="",end_date="",players=[],time_control=TIME_CONTROL["1"],description="",nb_of_rounds=4):
        self.name = name
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.nb_of_rounds = nb_of_rounds
        self.rounds = ["Round 1"]
        self.players = players
        self.time_control = time_control
        self.description = description
        Tournaments.all_tournaments.append(self)

    def add_players(self,player):
        self.players.append(player)


class Rounds:
    def __init__(self):
        self.name = name
        self.start_date = start_date
        self.start_time = start_time
        self.end_date = end_date
        self.end_time = end_time
        self.matches = []


class Matches:
    def __init__(self):
        self.players_pair = players_pair
        self.players_color = players_color


if __name__ == "__main__":
    pass