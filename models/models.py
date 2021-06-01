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
    def __init__(self, first_name="", family_name="", birth_date="",
                 sex="", ranking="", id = "", add_to_db=False):
        self.first_name = first_name
        self.family_name = family_name
        self.birth_date = birth_date
        self.sex = sex
        self.ranking = ranking
        self.id = id
        if add_to_db:
            serialized_player = {}
            for attributes in self.__dict__.items():
                serialized_player[attributes[0]] = attributes[1]
            DB.add_record("players", serialized_player)

    @classmethod
    def instantiate_from_db(cls,player_id):
        db_player = DB.get_record_data("players",player_id)
        new_player = cls(first_name=db_player["first_name"],
                         family_name=db_player["family_name"],
                         birth_date=db_player["birth_date"],
                         sex=db_player["sex"],
                         ranking=db_player["ranking"],
                         id=player_id)
        return new_player

    def add_player_to_tournament(self,tournament_id):
        players = DB.get_record_data("tournaments",tournament_id,"players")
        if len(players) >= 8:
            print("Ce tournoi compte déjà 8 joueurs.")
        else:
            DB.update_record_data("tournaments", tournament_id, "players", self.__dict__, True)

    def __str__(self):
        return (f"Players(first_name={self.first_name},"
              f"family_name={self.family_name},"
              f"birth_date={self.birth_date},"
              f"sex={self.sex},"
              f"ranking={self.ranking},"
              f"id={self.id})")



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
                 nb_of_rounds=4, rounds=[], players=[],
                 time_control=TIME_CONTROL["1"], description="",
                 id="",
                 add_to_db=False):
        self.name = name
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.nb_of_rounds = nb_of_rounds
        self.rounds = rounds
        self.players = players
        self.time_control = time_control
        self.description = description
        self.id = id
        if add_to_db:
            serialized_tournament = {}
            for attributes in self.__dict__.items():
                serialized_tournament[attributes[0]] = attributes[1]
            DB.add_record("tournaments",serialized_tournament)

    @classmethod
    def instantiate_from_db(cls,tournament_id):
        db_tournament = DB.get_record_data("tournaments",int(tournament_id))
        new_tournament = cls(name=db_tournament["name"],
                         place=db_tournament["place"],
                         start_date=db_tournament["start_date"],
                         end_date=db_tournament["end_date"],
                         nb_of_rounds=db_tournament["nb_of_rounds"],
                         rounds=db_tournament["rounds"],
                         players=db_tournament["players"],
                         time_control=db_tournament["time_control"],
                         description=db_tournament["description"],
                         id=tournament_id)
        return new_tournament

    def is_empty(self):
        """
        Check if no player is enlisted to the tournament
        Returns a boolean (True/False)

            Parameters
            ----------
                None

            Returns
            -------
                True if players list is empty or
                False otherwise
        """
        if len(self.players) == 0:
            print("Aucun joueur n'est inscrit au ", self.name,".",sep="")
            print()
            return True
        else:
            return False

    def is_full(self):
        """
        Check if a tournament has already 8 players
        enlisted hence is full
        Returns a boolean (True/False)

            Parameters
            ----------
                None

            Returns
            -------
                True if players list is made
                of 8 elements or False otherwise
        """
        if len(self.players) == 8:
            return True
        else:
            return False


    def new_pair(self,player1,player2):
        """
        Checks if a pair of players have already played against
        each other during a tournament
        Returns a boolean (True/False)

            Parameters
            ----------
                player1 -> a Players instance
                player2 -> a Players instance

            Returns
            -------
                True if player1 and player2 have never played
                against each other during the Tournament or
                False otherwise
        """
        rounds = self.rounds
        for round in rounds:
            for match in round["matches"]:
                if match[0][0] == player1 and match[1][0] == player2:
                    return False
                elif match[0][0] == player2 and match[1][0] == player1:
                    return False
        return True

    def tournament_ranking(self):
        """
        Generates players ranking for a Tournaments instance
        Returns a boolean (True/False)

            Parameters
            ----------
                None

            Returns
            -------
                A sorted list of the Tournament's players
                ranked by points and then by ranking if several
                players have the same number of points.
        """
        players = self.players
        new_ranking = []
        for player in players:
            new_ranking.append({"id":player["id"],"ranking":player["ranking"],"points":0})
        return sorted(new_ranking,key=lambda x: (x["points"],-int(x["ranking"])),reverse=True)

    def generate_round(self):
        """
        Add a new Rounds' instance into the Rounds list
        of a Tournament instance

            Parameters
            ----------
                None

            Returns
            -------
                None
        """
        rounds = self.rounds
        if len(rounds) < int(self.nb_of_rounds):
            round_number = len(rounds) + 1
            new_round = Rounds("Round " + str(round_number), TODAY, NOW)
            self.rounds.append(new_round.__dict__)
        else:
            print("Le tournoi a atteint son nombre maximal de rondes.")
        return

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
        """
        Checks if all round matches have been played hence
        if round is over
        Returns a boolean (True/False)

            Parameters
            ----------
                None

            Returns
            -------
                True if all round matches have been played
                or False otherwise
        """
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
        """
        Checks if a match has already been played or not
        Returns a boolean (True/False)

            Parameters
            ----------
                None

            Returns
            -------
                True if match has been played and sum
                of both players score is greater than 0
                or False otherwise
        """
        somme = self.pair[0][1] + self.pair[1][1]
        if somme > 0:
            return True
        else:
            return False

    def match_score(self,score_player1,score_player2):
        """
        Updates the score of a match

            Parameters
            ----------
                score_player1 -> match score of player1
                score_player2 -> match score of player2
                pair -> a list of tuples made of a Players instance
                and his/her match score

            Returns
            -------
                Nothing
        """
        self.pair = [(self.player1,score_player1),(self.player2,score_player2)]
        return

if __name__ == "__main__":
    pass
