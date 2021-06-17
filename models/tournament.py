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
                 rounds=[], players=[],
                 time_control=TIME_CONTROL["1"], description="",
                 id="",
                 add_to_db=False):
        self.name = name
        self.place = place
        self._start_date = start_date
        self._end_date = end_date
        self.nb_of_rounds = 4
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
                         rounds=db_tournament["rounds"],
                         players=db_tournament["players"],
                         time_control=db_tournament["time_control"],
                         description=db_tournament["description"],
                         id=tournament_id)
        return new_tournament

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
            instantiated_round = rn.Round().instantiate_from_dict(round)
            if not instantiated_round.round_played():
                liste.append(i)
        return liste

    @property
    def is_finished(self):
        for round in self.rounds:
            instantiated_round = rn.Round().instantiate_from_dict(round)
            if not instantiated_round.round_played():
                return False
        return True

    def check_status(self):
        if self.tournament_nb_of_rounds < self.nb_of_rounds:
            if len(self.tournament_unfinished_rounds_ids) == 0:
                self.generate_round()
                self.generate_matches()
                DB.update_record_data("tournaments",self._id,"rounds",self.rounds)
                print("Un nouveau round vient d'être généré pour ce tournoi.")
        elif self.tournament_nb_of_rounds == self.nb_of_rounds:
            if len(self.tournament_unfinished_rounds_ids) == 0:
                self._end_date = TODAY
                DB.update_record_data("tournaments", self._id, "_end_date", self._end_date)

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
                list_of_pairs.append((match[0][0]["id"],match[1][0]["id"]))
                list_of_pairs.append((match[1][0]["id"], match[0][0]["id"]))
        return list(set(list_of_pairs))

    def check_available_players(self):
        if len(self.available_players) == 0 and self.tournament_nb_of_players > 0:
            print("Tous les joueurs de la base sont déjà inscrits au", self.name, end=".\n")
            print("Merci de créer un nouveau joueur avant de l'inscrire au", self.name, end=".\n")
        else:
            print("Voici la liste des joueurs enregistrés non inscrits au", self.name, ":")
            for player in PLAYERS_TABLE:
                if player.doc_id not in self.tournament_players_ids:
                    print(player.doc_id, "->", player["first_name"], player["family_name"])

    def add_player_to_tournament(self,player_id):
        if player_id in self.tournament_players_ids:
            print("Ce joueur est déjà inscrit au ", self.name, ".",sep="")
        elif player_id not in self.available_players:
            print("Choix non valide.")
        else:
            new_player = pl.Player().instantiate_from_db(player_id)
            self.players.append(vars(new_player))
            DB.update_record_data("tournaments",self.id,"players",self.players)
            print(f"{new_player.first_name} {new_player.family_name} a été inscrit au {self.name}.")
            print(f"Le tournoi compte maintenant {self.tournament_nb_of_players} joueurs.")
            if self.tournament_nb_of_players == 8:
                self.generate_round()
                self.generate_matches()
                DB.update_record_data("tournaments",self.id,"rounds",self.rounds)
                print("Le premier round du tournoi a été généré.")

    def is_empty(self,display1=True,display2=True):
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
            if display1:
                print("Aucun joueur n'est inscrit au ", self.name,".",sep="")
            return True
        else:
            if display2:
                print("Voici les inscrits au", self.name, ":")
                for player in self.players:
                    print(player["_id"], "->", player["first_name"], player["family_name"])
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

    @property
    def tournament_scores(self):
        tournament_scores = {player["_id"]:0 for player in self.players}
        for round in self.rounds:
            for match in round["matches"]:
                for score in match:
                    tournament_scores[score[0]["id"]] += score[1]
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
            new_ranking.append({"player":player,"ranking":player["_ranking"],"points":tournament_scores[player["_id"]]})
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
        if self.tournament_nb_of_rounds < int(self.nb_of_rounds):
            round_number = len(rounds) + 1
            new_round = rn.Round("Round " + str(round_number), TODAY, NOW)
            self.rounds.append(vars(new_round))
        else:
            print("Le tournoi a atteint son nombre maximal de rondes.")
        return

    def generate_matches(self):
        matches = []
        players = self.players
        rounds = self.rounds
        if self.tournament_nb_of_rounds == 1:
            sorted_players = sorted(players, key=lambda x: x["_ranking"], reverse=False)
            for i in range(len(self.players)//2):
                match = ([sorted_players[i],0],[sorted_players[i + 4],0])
                new_match = mt.Match(match)
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
                    match = ([tournament_ranking[i],0],[tournament_ranking[j],0])
                    new_match = mt.Match(match)
                    matches.append(new_match.pair)
                    tournament_ranking.pop(j)
                    tournament_ranking.pop(i)
                    j = 1
                else:
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
