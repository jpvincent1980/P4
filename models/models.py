#! /usr/bin/env python3
# coding: utf-8

class Players:

    all_players = []

    def __init__(self, first_name, family_name, birth_date, sex, ranking):
        self.first_name = first_name
        self.family_name = family_name
        self.birth_date = birth_date
        self.sex = sex
        self.ranking = ranking
        Players.all_players.append(self)


TIME_CONTROL = {"1": "Bullet",
                "2": "Blitz",
                "3": "Coup rapide"}


class Tournaments:

    all_tournaments = []
    global TIME_CONTROL

    def __init__(self, name="", place="", start_date="", end_date="",
                 players=[],
                 time_control=TIME_CONTROL["1"], description="",
                 nb_of_rounds=4):
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

    def add_players(self, player):
        self.players.append(player)

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


if __name__ == "__main__":
    pass
