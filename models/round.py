#! /usr/bin/env python3
# coding: utf-8
from models import match as mt
from models import player as pl
import time


class Round:
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
            round_completed -> returns True if the round is over (i.e.
            all round's matches have been played) or False if not
            """
    def __init__(self, name="", start_date="", start_time="",
                 end_date="", end_time="", matches=[]):
        self.name = name
        self._start_date = start_date
        self._start_time = start_time
        self._end_date = end_date
        self._end_time = end_time
        self.matches = matches

    def __getitem__(self, item):
        return getattr(self, item)

    @classmethod
    def instantiate_from_serialized_round(cls,serialized_round):
        new_round = cls(name=serialized_round["name"],
                         start_date=serialized_round["_start_date"],
                         start_time=serialized_round["_start_time"],
                         end_date=serialized_round["_end_date"],
                         end_time=serialized_round["_end_time"],
                         matches=serialized_round["matches"])
        return new_round

    def serialize_round(self):
        serialized_round = {"name":self.name,
                            "_start_date":self._start_date,
                            "_start_time":self._start_time,
                            "_end_date":self._end_date,
                            "_end_time":self._end_time,
                            "matches":self.matches
                            }
        return serialized_round

    @property
    def list_of_unplayed_matches_ids(self):
        liste = []
        for i, match in enumerate(self.matches,start=1):
            player1 = pl.Player.instantiate_from_serialized_player(match[0][0])
            player2 = pl.Player.instantiate_from_serialized_player(match[1][0])
            score_player1 = match[0][1]
            score_player2 = match[1][1]
            instantiated_match = mt.Match(player1,player2,score_player1,score_player2)
            if not instantiated_match.match_completed():
                liste.append(i)
        return liste

    @property
    def round_completed(self):
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
            player1 = pl.Player.instantiate_from_serialized_player(match[0][0])
            player2 = pl.Player.instantiate_from_serialized_player(match[1][0])
            score_player1 = match[0][1]
            score_player2 = match[1][1]
            instantiated_match = mt.Match(player1,player2,score_player1,score_player2)
            if not instantiated_match.match_completed():
                return False
        return True


if __name__ == "__main__":
    pass
