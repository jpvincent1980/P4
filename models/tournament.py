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

    @classmethod
    def instantiate_from_db(cls,tournament_id):
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

    def serialize_tournament(self):
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

    @classmethod
    def available_tournaments(cls):
        available_tournaments = {}
        for tournament in TOURNAMENTS_TABLE:
            if len(tournament["players"])<8:
                available_tournaments[tournament["_id"]] = tournament["name"]
        return available_tournaments

    @classmethod
    def full_tournaments(cls):
        full_tournaments = []
        for tournament in TOURNAMENTS_TABLE:
            if len(tournament["players"]) >= 8:
                full_tournaments.append(tournament)
        return full_tournaments

    @classmethod
    def update_ids(cls):
        for tournament in TOURNAMENTS_TABLE:
            DB.update_record_data("tournaments",tournament.doc_id,"_id",tournament.doc_id)
        return

    @classmethod
    def list_of_ids(cls):
        return [tournament.doc_id for tournament in TOURNAMENTS_TABLE]

    @property
    def tournament_nb_of_players(self):
        return len(self.players)

    @property
    def tournament_nb_of_rounds(self):
        return len(self.rounds)

    @property
    def tournament_players_ids(self):
        return [player["_id"] for player in self.players]

    @property
    def tournament_rounds_ids(self):
        return [i+1 for i in range(len(self.rounds))]

    @property
    def tournament_unfinished_rounds_ids(self):
        liste = []
        for i,round in enumerate(self.rounds,start=1):
            instantiated_round = rn.Round().instantiate_from_serialized_round(round)
            if not instantiated_round.round_completed:
                liste.append(i)
        return liste

    @property
    def tournament_completed(self):
        if self.tournament_nb_of_rounds < self.nb_of_rounds:
            return False
        else:
            for round in self.rounds:
                instantiated_round = rn.Round().instantiate_from_serialized_round(round)
                if not instantiated_round.round_completed:
                    return False
            return True

    @classmethod
    def uncompleted_tournaments(cls):
        tournaments_list = []
        for tournament in Tournament.full_tournaments():
            tournament = Tournament.instantiate_from_serialized_tournament(tournament)
            if not tournament.tournament_completed:
                tournaments_list.append(tournament.serialize_tournament())
        return tournaments_list

    @classmethod
    def uncompleted_tournaments_ids(cls):
        tournaments_ids_list = []
        for tournament in Tournament.full_tournaments():
            tournament = Tournament.instantiate_from_serialized_tournament(tournament)
            if not tournament.tournament_completed:
                tournaments_ids_list.append(tournament.serialize_tournament()["_id"])
        return tournaments_ids_list

    @property
    def available_players_ids(self):
        all_players_id = []
        for player in pl.PLAYERS_TABLE.all():
            all_players_id.append(player.doc_id)
        available_players_id = list(set(all_players_id).difference(self.tournament_players_ids))
        return available_players_id

    @property
    def set_of_pairs(self):
        list_of_pairs = []
        for round in self.rounds:
            for match in round["matches"]:
                list_of_pairs.append((match[0][0]["_id"],match[1][0]["_id"]))
                list_of_pairs.append((match[1][0]["_id"], match[0][0]["_id"]))
        return list(set(list_of_pairs))

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

    @property
    def tournament_scores(self):
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
                ranked by points and then by ranking if several
                players have the same number of points.
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

    @classmethod
    def tournaments_list(cls):
        tournaments_list = []
        for tournament in TOURNAMENTS_TABLE:
            tournaments_list.append(tournament)
        return tournaments_list

    @classmethod
    def players_list_by_tournament(cls,tournament_id):
        players_list = []
        tournament = Tournament.instantiate_from_db(tournament_id)
        players = tournament.players
        for player in players:
            players_list.append(player)
        return players_list

if __name__ == "__main__":
    pass
