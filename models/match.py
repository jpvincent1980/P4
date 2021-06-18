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
            match_completed -> returns True if the match is over (i.e.
            sum of points of both players is greater than 0) or False if not
            match_score -> updates the score of the match
            """
    def __init__(self,player1,player2,score_player1=0,score_player2=0):
        self._player1 = player1
        self._player2 = player2
        self._score_player1 = score_player1
        self._score_player2 = score_player2

    def __str__(self):
        return f"{self._player1.first_name} {self._player1.family_name} vs " \
               f"{self._player2.first_name} {self._player2.family_name} \n " \
               f"Score -> {self._score_player1} - {self._score_player2}"

    @classmethod
    def instantiate_from_serialized_match(cls, serialized_match):
        new_match = cls(player1=serialized_match["_player1"],
                        player2=serialized_match["_player2"],
                        score_player1=serialized_match["_score_player1"],
                        score_player2=serialized_match["_score_player2"])
        return new_match

    def serialize_match(self):
        serialized_match = {"_player1":self._player1,
                            "_player2":self._player2,
                            "_score_player1":self._score_player1,
                            "_score_player2":self._score_player2}
        return serialized_match


    @property
    def pair(self):
        return [[pl.Player.serialize_player(self._player1),self._score_player1],
                [pl.Player.serialize_player(self._player2),self._score_player2]]

    def match_completed(self):
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
                score_player1 -> match score of player1
                score_player2 -> match score of player2
                pair -> a list of tuples made of a Players instance
                and his/her match score

            Returns
            -------
                Nothing
        """
        self._score_player1 = score_player1
        self._score_player2 = score_player2
        return

if __name__ == "__main__":
    pass
