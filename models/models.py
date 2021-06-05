#! /usr/bin/env python3
# coding: utf-8
from models import dbmanager
import time
import datetime

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
        self._id = id
        if add_to_db:
            serialized_player = {}
            for attributes in self.__dict__.items():
                serialized_player[attributes[0]] = attributes[1]
            DB.add_record("players", serialized_player)

    @property
    def birth_date(self):
        return self._birth_date

    @birth_date.setter
    def birth_date(self,date):
        try:
            datetime.datetime.strptime(date,"%d/%M/%Y")
            self._birth_date = date
        except ValueError:
            # print("La date doit être au format JJ/MM/AAAA.")
            self._birth_date = ""


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

    @classmethod
    def check_if_any_player(cls,display1=True,display2=True):
        if len(PLAYERS_TABLE) == 0:
            if display1 == True:
                print("Aucun joueur n'est enregistré dans la base de données.")
            return False
        else:
            if display2 == True:
                print("Voici la liste des joueurs enregistrés dans la base:")
                for player in PLAYERS_TABLE:
                    print(player.doc_id, "->", player["first_name"], player["family_name"],
                          "| Classement actuel ->", player["ranking"])
                print()
            return True

    @classmethod
    def list_of_ids(cls):
        return [player.doc_id for player in PLAYERS_TABLE]

    def __str__(self):
        return f"{self.first_name} {self.family_name}"



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
    def check_if_any_tournament(cls,display1=True,display2=True):
        if len(TOURNAMENTS_TABLE) == 0:
            if display1 == True:
                print("Aucun tournoi n'est créé dans la base de données.")
            return False
        else:
            if display2 == True:
                print("Voici la liste des tournois créés dans la base:")
                for tournament in TOURNAMENTS_TABLE:
                    print(tournament.doc_id, "->", tournament["name"])
            print()
            return True

    @property
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
        return [player["id"] for player in self.players]

    @property
    def tournament_rounds_ids(self):
        return [i+1 for i in range(len(self.rounds))]

    @property
    def tournament_unfinished_rounds_ids(self):
        liste = []
        for i,round in enumerate(self.rounds,start=1):
            instantiated_round = Rounds().instantiate_from_dict(round)
            if not instantiated_round.round_played():
                liste.append(i)
        return liste

    @property
    def is_finished(self):
        for round in self.rounds:
            instantiated_round = Rounds().instantiate_from_dict(round)
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

    def check_players(self):
        if self.tournament_nb_of_players == 0:
            print("Aucun joueur n'est inscrit au", self.name, "pour le moment.")
        elif self.tournament_nb_of_players > 0:
            if self.tournament_nb_of_players >= 8:
                print("Le tournoi est complet.")
            print("Voici la liste des joueurs déjà inscrits au", self.name, ":")
            for player in self.players:
                print(player["id"], "->", player["first_name"], player["family_name"])
                self.tournament_players_ids.append(player["id"])
        return

    @property
    def available_players(self):
        all_players_id = []
        for player in PLAYERS_TABLE.all():
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
            new_player = Players().instantiate_from_db(player_id)
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
                    print(player["id"], "->", player["first_name"], player["family_name"])
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
        tournament_scores = {player["id"]:0 for player in self.players}
        for round in self.rounds:
            for match in round["matches"]:
                for score in match:
                    tournament_scores[score[0]["id"]] += score[1]
        return tournament_scores


    @property
    def tournament_ranking(self):
        """
        Generates players ranking for a Tournaments instance
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
            new_ranking.append({"player":player,"ranking":player["ranking"],"points":tournament_scores[player["id"]]})
        new_ranking = sorted(new_ranking,key=lambda x: (x["points"],-int(x["ranking"])),reverse=True)
        new_ranking = [element["player"] for element in new_ranking]
        for player in new_ranking:
            player.update({"score":tournament_scores[player["id"]]})
        return new_ranking

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
        if self.tournament_nb_of_rounds < int(self.nb_of_rounds):
            round_number = len(rounds) + 1
            new_round = Rounds("Round " + str(round_number), TODAY, NOW)
            self.rounds.append(vars(new_round))
        else:
            print("Le tournoi a atteint son nombre maximal de rondes.")
        return

    def generate_matches(self):
        matches = []
        players = self.players
        rounds = self.rounds
        if self.tournament_nb_of_rounds == 1:
            sorted_players = sorted(players, key=lambda x: x["ranking"], reverse=False)
            for i in range(4):
                match = ([sorted_players[i],0],[sorted_players[i + 4],0])
                new_match = Matches(match)
                matches.append(new_match.pair)
            rounds[0]["matches"] = matches
            return matches
        else:
            tournament_ranking = self.tournament_ranking
            set_of_pairs = self.set_of_pairs
            j = 1
            while len(tournament_ranking) > 0:
                i = 0
                if (tournament_ranking[i]["id"], tournament_ranking[j]["id"]) not in set_of_pairs:
                    match = ([tournament_ranking[i],0],[tournament_ranking[j],0])
                    new_match = Matches(match)
                    matches.append(new_match.pair)
                    tournament_ranking.pop(j)
                    tournament_ranking.pop(i)
                    j = 1
                else:
                    j += 1
            rounds[-1]["matches"] = matches
            return matches


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
            instantiated_match = Matches(match)
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
            instantiated_match = Matches(match)
            if instantiated_match.match_played() is False:
                return False
        return True

class Matches:
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
            match_played -> returns True if the match is over (i.e.
            sum of points of both players is greater than 0) or False if not
            match_score -> updates the score of the match
            """
    def __init__(self,match):
        self._player1 = match[0][0]
        self._player2 = match[1][0]
        self._score_player1 = match[0][1]
        self._score_player2 = match[1][1]

    def __str__(self):
        return f"{self._player1['first_name']} {self._player1['family_name']} vs " \
               f"{self._player2['first_name']} {self._player2['family_name']} \n " \
               f"Score -> {self._score_player1} - {self._score_player2}"

    @property
    def pair(self):
        return [[self._player1,self._score_player1],[self._player2,self._score_player2]]

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
