#! /usr/bin/env python3
# coding: utf-8
from models import dbmanager
import datetime

DB = dbmanager.DBManager("db.json","tournaments","players")
PLAYERS_TABLE = DB.players


class Player:
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

    def __str__(self):
        """
        A magic method that displays a player's instance
        in a nice way when printed on user's terminal

            Returns
            ----------
                 a f'-string with player's first name and family name
        """
        return f"{self.first_name} {self.family_name}"

    @property
    def birth_date(self):
        """
        Returns player's birth_date

            Parameters
            ----------
                None

            Returns
            ----------
                Player's birth date
        """
        return self._birth_date

    @birth_date.setter
    def birth_date(self,new_birth_date):
        """
        Returns player's birth_date in a defined format:
        JJ/MM/AAAA

            Parameters
            ----------
                new_birth_date -> player's birth date

            Returns
            ----------
                Player's birth date in JJ/MM/AAAA format
        """
        try:
            datetime.datetime.strptime(new_birth_date,"%d/%M/%Y")
            self._birth_date = new_birth_date
        except ValueError:
            new_birth_date = input(f"La date doit être au format JJ/MM/AAAA:\n"
                         f">>> ")
            self._birth_date = new_birth_date

    @property
    def sex(self):
        """
        Returns player's sex

            Parameters
            ----------
                None

            Returns
            ----------
                Player' sex
        """
        return self._sex

    @sex.setter
    def sex(self,new_sex):
        """
        Returns player's sex in a defined format:
        'H' or 'F'

            Parameters
            ----------
                new_sex -> player's sex

            Returns
            ----------
                Player's sex as 'H' or 'F'
        """
        try:
            if new_sex.upper() == "H" or new_sex.upper() == "F":
                self._sex = new_sex.upper()
            else:
                raise ValueError
        except ValueError:
            new_sex = input(f"La réponse doit être H ou F:\n"
                  f">>> ")
            self._sex = new_sex.upper()

    @property
    def ranking(self):
        """
        Returns player's ranking

            Parameters
            ----------
                None

            Returns
            ----------
                Player's ranking
        """
        return self._ranking

    @ranking.setter
    def ranking(self,new_ranking):
        """
        Returns player's ranking as an integer >0

            Parameters
            ----------
                None

            Returns
            ----------
                Player's ranking
        """
        try:
            if int(new_ranking) > 0:
                self._ranking = new_ranking
            else:
                raise ValueError
        except ValueError:
            print(f"Le classement doit être un entier strictement supérieur à 0.")
            new_ranking = input(f"Entrez le nouveau classement:\n"
                         f">>> ")
            self._ranking = new_ranking

    @classmethod
    def instantiate_from_db(cls,player_id):
        """
        Creates a Player instance according to the attributes of a TinyDB document
        from the 'players' table

            Parameters
            ----------
                player_id -> the doc_id of a document from the 'players' TinyDB table
                representing a player

            Returns
            ----------
                A Player instance
        """
        db_player = DB.get_record_data("players",player_id)
        new_player = cls(first_name=db_player["first_name"],
                         family_name=db_player["family_name"],
                         birth_date=db_player["_birth_date"],
                         sex=db_player["_sex"],
                         ranking=db_player["_ranking"],
                         id=player_id)
        return new_player

    @classmethod
    def instantiate_from_serialized_player(cls, serialized_player):
        """
        Creates a Player instance according to the keys and values of
        a dictionary provided as an argument

            Parameters
            ----------
                serialized_player -> a dictionary that must contains the
                following keys -> first_name, family_name, _birth_date,
                _sex, _ranking and _id

            Returns
            ----------
                A Player instance
        """
        new_player = cls(first_name=serialized_player["first_name"],
                         family_name=serialized_player["family_name"],
                         birth_date=serialized_player["_birth_date"],
                         sex=serialized_player["_sex"],
                         ranking=serialized_player["_ranking"],
                         id=serialized_player["_id"])
        return new_player

    @classmethod
    def list_of_ids(cls):
        """
        Returns the ids of all players created in the TinyDB database in a list.
        Each player id is equal to its corresponding TinyDB document doc_id.

            Parameters
            ----------
                None

            Returns
            ----------
                A list of integers representing all players created in the TinyDB database
        """
        return [player.doc_id for player in PLAYERS_TABLE]

    @classmethod
    def update_ids(cls):
        """
        Updates the '_id' value of each player of the 'players' TinyDB table with
        its corresponding document doc_id.

            Parameters
            ----------
                None

            Returns
            ----------
                None
        """
        for player in PLAYERS_TABLE:
            DB.update_record_data("players",player.doc_id,"_id",player.doc_id)
        return

    @classmethod
    def players_list(cls,sorting_choice):
        """
        Returns a list of serialized players sorted
        by alphabetical or ranking order

            Parameters
            ----------
                sorting_choice -> '1' for alphabetical
                order or '2' for ranking order

            Returns
            ----------
                A list of serialized players sorted
                according to user's choice
        """
        players_list = []
        sorting_choice = int(sorting_choice)
        if sorting_choice == 1:
            for player in sorted(PLAYERS_TABLE, key=lambda x: x['family_name']):
                players_list.append(player)
        elif sorting_choice == 2:
            for player in sorted(PLAYERS_TABLE, key=lambda x: int(x['_ranking'])):
                players_list.append(player)
        return players_list

    def serialize_player(self):
        """
        Converts a player instance into a dictionary

            Parameters
            ----------
                None

            Returns
            ----------
                A dictionary with the instance attributes as keys
                and their values as keys' values
        """
        serialized_player = {"first_name":self.first_name,
                             "family_name":self.family_name,
                             "_birth_date":self._birth_date,
                             "_sex":self._sex,
                             "_ranking":self._ranking,
                             "_id":self._id}
        return serialized_player


if __name__ == "__main__":
    pass
