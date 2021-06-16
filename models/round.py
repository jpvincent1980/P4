#! /usr/bin/env python3
# coding: utf-8
from models import match as mt
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
            round_played -> returns True if the round is over (i.e.
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
    def instantiate_from_dict(cls,round_dict):
        new_round = cls(name=round_dict["name"],
                         start_date=round_dict["_start_date"],
                         start_time=round_dict["_start_time"],
                         end_date=round_dict["_end_date"],
                         end_time=round_dict["_end_time"],
                         matches=round_dict["matches"])
        return new_round

    @property
    def list_of_unplayed_matches_ids(self):
        liste = []
        for i, match in enumerate(self.matches,start=1):
            instantiated_match = mt.Match(match)
            if not instantiated_match.match_played():
                liste.append(i)
        return liste


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
            instantiated_match = mt.Match(match)
            if instantiated_match.match_played() is False:
                return False
        return True


if __name__ == "__main__":
    pass
