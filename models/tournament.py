#! /usr/bin/env python3
# coding: utf-8
from models import dbmanager
from models import player as pl
from models import round as rn
from models import match as mt
import time

TIME_CONTROL = {"1": "Bullet",
                "2": "Blitz",
                "3": "Coup rapide"}

DB = dbmanager.DBManager("db.json","tournaments","players")
TOURNAMENTS_TABLE = DB.tournaments
TODAY = time.strftime("%d/%m/%Y")
NOW = time.strftime("%Hh%Mm%Ss")


class Tournament:
    """
    A class that represents a tournament.

        Attributes
        ----------
            name -> name of the tournament
            place -> name of the place where the tournament takes place
            _start_date -> start date of the tournament
            _end_date -> end date of the tournament
            nb_of_rounds  -> number of rounds of the tournament (4 by default)
            rounds -> list of tournament's rounds
            players -> list of tournament's players
            time_control -> type of time control (Bullet, Blitz or Coup Rapide)
            description -> description of the tournament
            _id -> identifier of the tournament

        Methods
        -------
            tournament_nb_of_players -> returns the number of
            players currently enlisted
            tournament_nb_of_rounds -> returns the number of
            rounds currently generated
            tournament_players_ids -> returns the list of ids of
            players already enlisted
            tournament_rounds_ids -> returns the list of ids of
            rounds already generated
            tournament_uncompleted_rounds_ids -> returns the
            list of ids of rounds uncompleted
            tournament_completed -> returns True if tournament
            is completed, False otherwise
            available_players_ids -> returns the list of ids of
            players not enlisted to the tournament
            set_of_pairs -> returns the list of players ids that
            have already played against each other (as tuples
            containing both ids)
            tournament_scores -> returns a dictionary with
            players' ids as key and their accumulated score
            as value
            tournament_ranking -> returns a sorted list of
            players depending on their results during the
            tournament
            instantiate_from_db -> creates a Tournament
            instance from a TinyDB document of the
            'tournaments' table
            instantiate_from_serialized_tournament -> creates
            a Tournament instance from a dictionary
            available_tournaments -> returns a list of
            serialized tournaments that have less than 8 players
            enlisted
            full_tournaments -> returns a list of serialized
            tournaments that have at least 8 players enlisted
            update_ids -> updates the '_id' attribute of a
            tournament with its corresponding document doc_id
            list_of_ids -> returns the list of tournaments' ids
            for tournaments created in the TinyDB database
            uncompleted_tournaments -> returns a list of
            serialized uncompleted tournaments
            uncompleted_tournaments_ids -> returns a list of
            tournaments' ids of uncompleted tournaments
            tournaments_list -> returns a list of serialized
            tournaments created in the TinyDB database
            uncompleted_rounds -> returns the list of Round instances
            that are uncompleted
            serialize_tournament -> returns a dictionary from
            a Tournament instance
            generate_round -> generates a round instance inside
            the rounds parameter of a Tournament instance
            generate_matches -> generates all matches of a round
    """
    global TIME_CONTROL, DB, TOURNAMENTS_TABLE
    def __init__(self, name="", place="", start_date=TODAY, end_date="",
                 nb_of_rounds=4, rounds=[], players=[],
                 time_control="", description="",
                 id="",
                 add_to_db=False):
        """
        Constructor of the Tournament class

            Parameters
            ----------
                name -> name of the tournament
                place -> name of the place where the tournament takes place
                _start_date -> start date of the tournament automatically assigned by the program
                _end_date -> end date of the tournament automatically assigned by the program
                nb_of_rounds  -> number of rounds of the tournament (by default = 4)
                rounds -> list of tournament's rounds
                players -> list of tournament's players
                time_control -> type of time control (Bullet, Blitz or Coup Rapide)
                description -> description of the tournament
                _id -> identifier of the tournament
                add_to_DB -> a boolean that defines if the tournament must be added
                to the TinyDB database
        """
        self.name = name
        self.place = place
        self._start_date = start_date
        self._end_date = end_date
        self.nb_of_rounds = nb_of_rounds
        self.rounds = rounds
        self.players = players
        self.time_control = time_control
        self.description = description
        self._id = id
        if add_to_db:
            serialized_tournament = {}
            for attributes in self.__dict__.items():
                serialized_tournament[attributes[0]] = attributes[1]
            DB.add_record("tournaments",serialized_tournament)

    @property
    def tournament_nb_of_players(self):
        """
        A property that returns the number of players already
        enlisted to the tournament

            Parameters
            ----------
                None

            Returns
            -------
                An integer representing the number of players already
                enlisted to the tournament
        """
        return len(self.players)

    @property
    def tournament_nb_of_rounds(self):
        """
        A property that returns the number of rounds already
        generated for the tournament

            Parameters
            ----------
                None

            Returns
            -------
                An integer representing the number of rounds already
                generated for the tournament's instance
        """
        return len(self.rounds)

    @property
    def tournament_players_ids(self):
        """
        A property that returns the ids of the players already
        enlisted to the tournament

            Parameters
            ----------
                None

            Returns
            -------
                A list of integers representing the players ids
        """
        return [player["_id"] for player in self.players]

    @property
    def tournament_rounds_ids(self):
        """
        A property that returns the ids of the tournament's rounds currently
        generated in a list

            Parameters
            ----------
                None

            Returns
            -------
                A list of integers representing the tournament's round ids
        """
        return [i+1 for i in range(len(self.rounds))]

    @property
    def tournament_uncompleted_rounds_ids(self):
        """
        Returns the ids of the tournament's rounds that are not
        completed yet (i.e. that have at least one match uncompleted)

            Parameters
            ----------
                None

            Returns
            -------
                A list of integers representing the round ids of uncompleted rounds
        """
        rounds_list = []
        for i,round in enumerate(self.rounds,start=1):
            instantiated_round = rn.Round().instantiate_from_serialized_round(round)
            if not instantiated_round.round_completed:
                rounds_list.append(i)
        return rounds_list

    @property
    def tournament_completed(self):
        """
        Returns True if all rounds of the tournament's instance
        are completed, otherwise False

            Parameters
            ----------
                None

            Returns
            -------
                A boolean -> True if all tournament's round are completed or
                False if at least one tournament's round is not completed
        """
        if self.tournament_nb_of_rounds < self.nb_of_rounds:
            return False
        else:
            for round in self.rounds:
                instantiated_round = rn.Round().instantiate_from_serialized_round(round)
                if not instantiated_round.round_completed:
                    return False
            return True

    @property
    def available_players_ids(self):
        """
        Retrieves the list of players' ids that are not enlisted
        to the tournament

            Parameters
            ----------
                None

            Returns
            -------
                A list of integers representing players' ids from the TinyDB 'players'
                table that are not enlisted in the tournament
        """
        all_players_id = []
        for player in pl.PLAYERS_TABLE.all():
            all_players_id.append(player.doc_id)
        available_players_id = list(set(all_players_id).difference(self.tournament_players_ids))
        return available_players_id

    @property
    def set_of_pairs(self):
        """
        Retrieves ids of players that have already played against
        each other during a tournament and creates two tuples for
        each duo (e.g. (2,4) and (4,2) if players 2 and 4 have played
        against each other)

            Parameters
            ----------
                None

            Returns
            -------
                A list of unique tuples made of both players' ids
        """
        list_of_pairs = []
        for round in self.rounds:
            for match in round["matches"]:
                list_of_pairs.append((match[0][0]["_id"],match[1][0]["_id"]))
                list_of_pairs.append((match[1][0]["_id"], match[0][0]["_id"]))
        return list(set(list_of_pairs))

    @property
    def tournament_scores(self):
        """
        Calculates the accumulated score of each player enlisted
        in a tournament by adding the points of all their matches
        played during that tournament

            Parameters
            ----------
                None

            Returns
            -------
                A dictionary made of players' id as key and their accumulated
                score as value
        """
        tournament_scores = {player["_id"]:0 for player in self.players}
        for round in self.rounds:
            for match in round["matches"]:
                for score in match:
                    tournament_scores[score[0]["_id"]] += score[1]
        return tournament_scores

    @property
    def tournament_ranking(self):
        """
        Generates players ranking for a Tournament instance
        Returns a list

            Parameters
            ----------
                None

            Returns
            -------
                A sorted list of the Tournament's players
                ranked by points accumulated during the tournament
                and then by ranking if several players have
                the same number of points.
        """
        tournament_scores = self.tournament_scores
        players = self.players
        new_ranking = []
        for player in players:
            new_ranking.append({"player":player,"_ranking":player["_ranking"],"points":tournament_scores[player["_id"]]})
        new_ranking = sorted(new_ranking,key=lambda x: (x["points"],-int(x["_ranking"])),reverse=True)
        new_ranking = [element["player"] for element in new_ranking]
        for player in new_ranking:
            player.update({"score":tournament_scores[player["_id"]]})
        return new_ranking

    @classmethod
    def instantiate_from_db(cls,tournament_id):
        """
        Creates a tournament instance according to the attributes of a TinyDB document
        from the 'tournaments' table

            Parameters
            ----------
                tournament_id -> the doc_id of a document from the 'tournaments" TinyDB table
                representing a tournament

            Returns
            ----------
                A tournament instance
        """
        db_tournament = DB.get_record_data("tournaments",int(tournament_id))
        new_tournament = cls(name=db_tournament["name"],
                         place=db_tournament["place"],
                         start_date=db_tournament["_start_date"],
                         end_date=db_tournament["_end_date"],
                         nb_of_rounds=db_tournament["nb_of_rounds"],
                         rounds=db_tournament["rounds"],
                         players=db_tournament["players"],
                         time_control=db_tournament["time_control"],
                         description=db_tournament["description"],
                         id=tournament_id)
        return new_tournament

    @classmethod
    def instantiate_from_serialized_tournament(cls,serialized_tournament):
        """
        Creates a tournament instance according to the keys and values of
        a dictionary provided as an argument

            Parameters
            ----------
                serialized_tournament -> a dictionary that must contains the
                following keys -> name, place, _start_date, _end_date, nb_of_rounds,
                rounds, players, time_control, description and _id

            Returns
            ----------
                A tournament instance
        """
        new_tournament = cls(name=serialized_tournament["name"],
                             place=serialized_tournament["place"],
                             start_date=serialized_tournament["_start_date"],
                             end_date=serialized_tournament["_end_date"],
                             nb_of_rounds=serialized_tournament["nb_of_rounds"],
                             rounds=serialized_tournament["rounds"],
                             players=serialized_tournament["players"],
                             time_control=serialized_tournament["time_control"],
                             description=serialized_tournament["description"],
                             id=serialized_tournament["_id"])
        return new_tournament

    @classmethod
    def available_tournaments(cls):
        """
        Returns tournament's id and name for tournaments
        that have less than 8 players enlisted as a dictionary consisting of
        tournament's id as key and tournament's name as value.

            Parameters
            ----------
                None

            Returns
            ----------
                A list of dictionaries consisting of tournament's id as key
                and tournament's name as value
        """
        available_tournaments = {}
        for tournament in TOURNAMENTS_TABLE:
            if len(tournament["players"]) < 8:
                available_tournaments[tournament["_id"]] = tournament["name"]
        return available_tournaments

    @classmethod
    def full_tournaments(cls):
        """
        Returns the list of serialized tournaments from the TinyDB database
        that have at least 8 players enlisted

            Parameters
            ----------
                None

            Returns
            ----------
                A list of serialized tournaments that have at least 8 players enlisted
        """
        full_tournaments = []
        for tournament in TOURNAMENTS_TABLE:
            if len(tournament["players"]) >= 8:
                full_tournaments.append(tournament)
        return full_tournaments

    @classmethod
    def update_ids(cls):
        """
        Updates the '_id' value of each tournament of the 'tournaments' TinyDB table with
        its corresponding document doc_id.

            Parameters
            ----------
                None

            Returns
            ----------
                None
        """
        for tournament in TOURNAMENTS_TABLE:
            DB.update_record_data("tournaments", tournament.doc_id, "_id", tournament.doc_id)
        return

    @classmethod
    def list_of_ids(cls):
        """
        Returns the ids of all tournaments created in the TinyDB database in a list.
        Each tournament id is equal to its corresponding TinyDB document doc_id.

            Parameters
            ----------
                None

            Returns
            ----------
                A list of integers representing all tournaments created in the TinyDB database
        """
        return [tournament.doc_id for tournament in TOURNAMENTS_TABLE]

    @classmethod
    def uncompleted_tournaments(cls):
        """
        Returns uncompleted serialized tournaments in a list. An uncompleted tournament
        is a tournament that has at least one uncompleted match.

            Parameters
            ----------
                None

            Returns
            ----------
                A list of dictionaries representing uncompleted serialized tournaments
        """
        tournaments_list = []
        for tournament in Tournament.full_tournaments():
            tournament = Tournament.instantiate_from_serialized_tournament(tournament)
            if not tournament.tournament_completed:
                tournaments_list.append(tournament.serialize_tournament())
        return tournaments_list

    @classmethod
    def uncompleted_tournaments_ids(cls):
        """
        Returns the ids of uncompleted tournaments in a list. An uncompleted tournament
        is a tournament that has at least one uncompleted match.

            Parameters
            ----------
                None

            Returns
            ----------
                A list of integers representing uncompleted tournaments ids
        """
        tournaments_ids_list = []
        for tournament in Tournament.full_tournaments():
            tournament = Tournament.instantiate_from_serialized_tournament(tournament)
            if not tournament.tournament_completed:
                tournaments_ids_list.append(tournament.serialize_tournament()["_id"])
        return tournaments_ids_list

    @classmethod
    def tournaments_list(cls):
        """
        Returns the list of tournaments created in the TinyDB database

            Parameters
            ----------
                None

            Returns
            ----------
                A list of serialized tournaments created in the TinyDB database
        """
        tournaments_list = []
        for tournament in TOURNAMENTS_TABLE:
            tournaments_list.append(tournament)
        return tournaments_list

    def uncompleted_rounds(self):
        """
        Returns the list of Round objects of a Tournament instance that are not completed (i.e.
        there is at least one match of that round for which the sum of players' score is
        equal to 0)

            Parameters
            ----------
                tournament -> a Tournament instance

            Returns
            ----------
                A list of Rounds objects if those rounds are not completed (round_completed method returns
                False)
        """
        rounds_list = []
        for round in self.rounds:
            round = rn.Round.instantiate_from_serialized_round(round)
            if not round.round_completed:
                rounds_list.append(round)
        return rounds_list

    def serialize_tournament(self):
        """
        Converts a tournament instance into a dictionary

            Parameters
            ----------
                None

            Returns
            ----------
                A dictionary with the instance attributes as keys
                and their values as keys' values
        """
        serialized_tournament = {"name":self.name,
                                 "place":self.place,
                                 "_start_date": self._start_date,
                                 "_end_date": self._end_date,
                                 "nb_of_rounds": self.nb_of_rounds,
                                 "rounds" : self.rounds,
                                 "players": self.players,
                                 "time_control": self.time_control,
                                 "description": self.description,
                                 "_id": self._id}
        return serialized_tournament

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

    def generate_round(self):
        """
        Add a new Round instance into the Rounds list
        of a Tournament instance

            Parameters
            ----------
                None

            Returns
            -------
                None
        """
        rounds = self.rounds
        round_number = len(rounds) + 1
        new_round = rn.Round("Round " + str(round_number), TODAY, NOW)
        self.rounds.append(vars(new_round))
        return

    def generate_matches(self):
        """
        Returns a list of matches for a given tournament's round. Matches are determined
        according to two rules: for the first round, all tournament's players are sorted
        by their ranking and split into two halves, best players of each half play against
        each others (e.g. first players of each half, second players of each half, etc.).
        For other rounds, each player is ranked by the number of points accumulated during
        the current tournament and then by ranking. The highest-ranked player plays against
        the next best player if they haven't played against each other sooner in the tournament

            Parameters
            ----------
                None

            Returns
            ----------
                A list of matches
        """
        matches = []
        players = self.players
        rounds = self.rounds
        if self.tournament_nb_of_rounds == 1:
            sorted_players = sorted(players, key=lambda x: x["_ranking"], reverse=False)
            for i in range(len(self.players)//2):
                player1 = pl.Player.instantiate_from_serialized_player(sorted_players[i])
                player2 = pl.Player.instantiate_from_serialized_player(sorted_players[i + 4])
                new_match = mt.Match(player1, player2, 0, 0)
                matches.append(new_match.pair)
            rounds[0]["matches"] = matches
            return matches
        else:
            tournament_ranking = self.tournament_ranking
            set_of_pairs = self.set_of_pairs
            j = 1
            while len(tournament_ranking) > 0:
                i = 0
                if (tournament_ranking[i]["_id"], tournament_ranking[j]["_id"]) not in set_of_pairs:
                    player1 = pl.Player.instantiate_from_serialized_player(tournament_ranking[i])
                    player2 = pl.Player.instantiate_from_serialized_player(tournament_ranking[j])
                    new_match = mt.Match(player1, player2, 0, 0)
                    matches.append(new_match.pair)
                    tournament_ranking.pop(j)
                    tournament_ranking.pop(i)
                    j = 1
                else:
                    if len(tournament_ranking) == 2:
                        player1 = pl.Player.instantiate_from_serialized_player(tournament_ranking[0])
                        player2 = pl.Player.instantiate_from_serialized_player(tournament_ranking[1])
                        new_match = mt.Match(player1, player2, 0, 0)
                        matches.append(new_match.pair)
                        tournament_ranking.pop(1)
                        tournament_ranking.pop(0)
                    j += 1
            rounds[-1]["matches"] = matches
            return matches

if __name__ == "__main__":
    pass
