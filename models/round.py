#! /usr/bin/env python3
# coding: utf-8
from models import match as mt
from models import player as pl


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
            instantiate_from_serialized_round -> creates a Round instance form a dictionary
            list_of_uncompleted_matches_ids -> returns the list of ids of uncompleted matches
            round_completed -> returns True if the round is over (i.e.
            all round's matches have been played) or False if not
            serialize_round -> creates a dictionary from a Round instance
    """
    def __init__(self, name="", start_date="", start_time="",
                 end_date="", end_time="", matches=[]):
        """
        Constructor of the Round class

            Parameters
            ----------
                name -> name of the round
                _start_date ->  start date of the round automatically assigned by program
                _start_time ->  start time of the round automatically assigned by program
                _end_date ->  end date of the round automatically assigned by program
                _end_time ->  end time of the round automatically assigned by program
                matches -> list of matches
        """
        self.name = name
        self._start_date = start_date
        self._start_time = start_time
        self._end_date = end_date
        self._end_time = end_time
        self.matches = matches

    def __getitem__(self, attribute):
        """
        A magic method that returns an attribute's value
        when calling instance_name["attribute"]

            Attributes
            ----------
                attribute -> name of the attribute

            Returns
            ----------
                Value of the attribute
        """
        return getattr(self, attribute)

    @classmethod
    def instantiate_from_serialized_round(cls,serialized_round):
        """
        Creates a round instance according to the keys and values of
        a dictionary provided as an argument

            Parameters
            ----------
                serialized_round -> a dictionary that must contains the
                following keys -> name, _start_date, _start_time, _end_date
                and _end_time

            Returns
            ----------
                A round instance
        """
        new_round = cls(name=serialized_round["name"],
                         start_date=serialized_round["_start_date"],
                         start_time=serialized_round["_start_time"],
                         end_date=serialized_round["_end_date"],
                         end_time=serialized_round["_end_time"],
                         matches=serialized_round["matches"])
        return new_round

    @property
    def list_of_uncompleted_matches_ids(self):
        """
        Returns a list of the id's of the round matches that
        are not completed yet (i.e. sum of both players' scores
        is equal to 0)

            Parameters
            ----------
                None

            Returns
            -------
                A list of ids
        """
        matches_list = []
        for i, match in enumerate(self.matches,start=1):
            player1 = pl.Player.instantiate_from_serialized_player(match[0][0])
            player2 = pl.Player.instantiate_from_serialized_player(match[1][0])
            score_player1 = match[0][1]
            score_player2 = match[1][1]
            instantiated_match = mt.Match(player1,player2,score_player1,score_player2)
            if not instantiated_match.match_completed():
                matches_list.append(i)
        return matches_list

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

    def serialize_round(self):
        """
        Converts a round instance into a dictionary

            Parameters
            ----------
                None

            Returns
            ----------
                A dictionary with the instance attributes as keys
                and their values as keys' values
        """
        serialized_round = {"name":self.name,
                            "_start_date":self._start_date,
                            "_start_time":self._start_time,
                            "_end_date":self._end_date,
                            "_end_time":self._end_time,
                            "matches":self.matches
                            }
        return serialized_round


if __name__ == "__main__":
    pass
