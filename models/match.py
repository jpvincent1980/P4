#! /usr/bin/env python3
# coding: utf-8
from models import player as pl

POINTS = {"Match perdu":0,
          "Match nul":0.5,
          "Match gagné":1}

POINTS_LIST = list(POINTS.values())


class Match:
    """
    A class that represents a round's match.

        Attributes
        ----------
            player1 -> player data for the first player of the match
            player2 -> player data for the second player of the match
            pair -> a list of two tuples, each tuple representing a player
            and its score

        Methods
        -------
            instantiate_from_serialized_match -> a class method that returns
            a Match instance from a dictionary
            serialize_match -> a method that returns a dictionary from a
            Match instance
            pair -> a property that returns a tuple of two lists, each list
            containing a player's instance and the player' score
            match_completed -> returns True if the match is over (i.e.
            sum of points of both players is greater than 0) or False if not
            match_score -> updates the score a match
    """
    def __init__(self,player1,player2,score_player1=0,score_player2=0):
        """
        Constructor of the Match class

            Parameters
            ----------
                player1 ->  a player instance representing player # 1
                player2 ->  a player instance representing player # 2
                score_player1 -> an integer or a float representing player # 1' score
                score_player2 -> an integer or a float representing player # 2' score

            Returns
            ----------
                None
        """
        self._player1 = player1
        self._player2 = player2
        self._score_player1 = score_player1
        self._score_player2 = score_player2

    def __str__(self):
        """
        A magic method that displays a match instance
        in a nice way when printed on user's terminal

            Parameters
            ----------
                None

            Returns
            ----------
                 a f'-string with both players full name and score
        """
        return f"{self._player1.first_name} {self._player1.family_name} vs " \
               f"{self._player2.first_name} {self._player2.family_name} \n " \
               f"Score -> {self._score_player1} - {self._score_player2}"

    @classmethod
    def instantiate_from_serialized_match(cls, serialized_match):
        """
        Creates a match instance according to the keys and values of
        a dictionary provided as an argument

            Parameters
            ----------
                serialized_match -> a dictionary that must contains the
                following keys -> _player1, _player2, _score_player1 and
                _score_player2

            Returns
            ----------
                A match instance
        """
        new_match = cls(player1=serialized_match["_player1"],
                        player2=serialized_match["_player2"],
                        score_player1=serialized_match["_score_player1"],
                        score_player2=serialized_match["_score_player2"])
        return new_match

    def serialize_match(self):
        """
        Converts a match instance into a dictionary

            Parameters
            ----------
                None

            Returns
            ----------
                A dictionary with the instance attributes as keys
                and their values as keys' values
        """
        serialized_match = {"_player1":self._player1,
                            "_player2":self._player2,
                            "_score_player1":self._score_player1,
                            "_score_player2":self._score_player2}
        return serialized_match


    @property
    def pair(self):
        """
        A property that returns a tuple of two lists, each list
        containing a player's instance and the player' score

            Parameters
            ----------
                None

            Returns
            ----------
                A tuple of two lists
        """
        return ([pl.Player.serialize_player(self._player1),self._score_player1],
                [pl.Player.serialize_player(self._player2),self._score_player2])

    def match_completed(self):
        """
        Checks if a match is completed or not
        Returns a boolean (True/False)

            Parameters
            ----------
                None

            Returns
            -------
                True if match is completed (i.e. sum
                of both players' score is greater than 0
                or False otherwise)
        """
        somme = self._score_player1 + self._score_player2
        if somme > 0:
            return True
        else:
            return False

    def match_score(self,score_player1,score_player2):
        """
        Updates the score of a match

            Parameters
            ----------
                score_player1 -> score of player1
                score_player2 -> score of player2
                pair -> a tuple made of two lists, each list containing
                a player instance and the player' score

            Returns
            -------
                Nothing
        """
        self._score_player1 = score_player1
        self._score_player2 = score_player2
        return

if __name__ == "__main__":
    pass
