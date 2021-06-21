#! /usr/bin/env python3
# coding: utf-8
from controllers import controller as ct
from models import player as pl
from models import tournament as tr

SORTING_MENU = {"1": "Ordre alphabétique",
                "2": "Classement"}


class View:
    """
    Main View class to display messages to user

        Attributes
        ----------
            None

        Methods
        -------
            show_title -> prints the opening message
            show_choice_message -> asks user to make a choice among
            the menu's lists
            back_to_homepage -> asks user to press Enter to go back to HomePage
    """
    def __init__(self):
        """
        Constructor of the View class
        """
        pass

    @classmethod
    def show_title(cls):
        """
        Prints the opening message
        """
        symbol = "+"
        title = "Gestionnaire de tournoi d'échecs"
        print(symbol * (len(title) + 6))
        print(symbol * 2,
              f"{title.upper()}",
              symbol * 2)
        print(symbol * (len(title) + 6))
        print()

    @classmethod
    def show_choice_message(cls):
        """
        Asks user to make a choice among the menu's lists
        """
        print("Merci de bien vouloir faire votre choix parmi le menu "
              "ci-dessous:")

    @classmethod
    def back_to_homepage(cls):
        """
        Asks user to press Enter to go back to HomePage
        """
        print()
        print("Tapez Entrée pour revenir au menu principal.")
        input(">>> ")
        return HomePage()


class HomePage(View):
    """
    Displays main menu and asks user to make a choice

        Attributes
        ----------
            None

        Methods
        -------
            show_message -> prints a message to user
            ask_user_choice -> waiting for user's input
    """
    def show_message(self):
        """
        Prints the main menu
        """
        self.menu = ct.MAIN_MENU
        self.show_choice_message()
        for key in self.menu.items():
            print(key[0], ": ", key[1])

    def ask_user_choice(self):
        """
        Waiting for user's input
        """
        return input(">>> ")


class CreateTournamentView(View):
    """
    Displays tournament creation view to user and asks for tournament's data

        Attributes
        ----------
            None

        Methods
        -------
            show_message -> prints a message to user
            ask_user_choice -> waiting for user's input
    """
    def show_message(self):
        """
        Prints message to user
        """
        print("Vous allez créer un nouveau tournoi.")

    def ask_user_choice(self):
        """
        Asks user to enter tournament's data
        """
        self.name = input("Entrez le nom du tournoi -> ")
        self.place = input("Entrez le lieu où se déroule le tournoi -> ")
        self.time_control = input(f"Entrez le numéro du type de contrôle "
                                  f"du temps :\n"
                                  f"{tr.TIME_CONTROL}\n"
                                  f">>> ")
        self.description = input("Entrez une description du tournoi -> ")
        return "0"


class TournamentCreationValidationView(View):
    """
    Displays tournament creation validation message

        Attributes
        ----------
            tournament_name -> name of the tournament

        Methods
        -------
            show_message -> prints a message to user
            ask_user_choice -> asks user to press Enter to go back to HomePage
    """
    def __init__(self, tournament_name):
        """
        Displays confirmation to user that tournament has been created

            Parameters
            ----------
                tournament_name -> name of the tournament

        """
        self.tournament_name = tournament_name

    def show_message(self):
        """
        Prints message to user
        """
        print(f"{self.tournament_name} a bien été créé dans notre base.")

    def ask_user_choice(self):
        """
        Asks user to press Enter to go back to HomePage
        """
        self.back_to_homepage()
        return HomePage()


class CreatePlayerView(View):
    """
    Asks user to create a new player

        Attributes
        ----------
            None

        Methods
        -------
            show_message -> prints a message to user
            ask_user_choice -> asks user to enter player's data
    """
    def show_message(self):
        """
        Prints message to user
        """
        print("Vous allez créer un nouveau joueur.")

    def ask_user_choice(self):
        """
        Asks user to enter player's data
        """
        self.first_name = input("Entrez le prénom du joueur -> ")
        self.family_name = input("Entrez le nom du joueur -> ")
        self.birth_date = input("Entrez la date de naissance du joueur "
                                "(JJ/MM/AAAA) -> ")
        self.sex = input("Entrez le sexe du joueur (H/F) -> ")
        self.ranking = input("Entrez le classement du joueur -> ")
        return "0"


class PlayerCreationValidationView(View):
    """
    Displays player creation validation message

        Attributes
        ----------
            new_player -> Player instance

        Methods
        -------
            show_message -> prints a message to user
            ask_user_choice -> asks user to press Enter to go back to HomePage
    """
    def __init__(self, new_player):
        """
        Displays confirmation to user that player has been created

            Parameters
            ----------
                new_player -> player's instance

        """
        self.new_player = new_player

    def show_message(self):
        """
        Prints message to user
        """
        print(f"{self.new_player.first_name} {self.new_player.family_name} "
              f"a bien été créé dans notre base.")

    def ask_user_choice(self):
        """
        Asks user to press Enter to go back to HomePage
        """
        self.back_to_homepage()
        return HomePage()


class AddPlayerToTournamentView(View):
    """
    Displays tournaments that are not full (i.e. number
    of players is less than 8) and asks user to choose one

        Attributes
        ----------
            None

        Methods
        -------
            show_message -> prints a message to user
            ask_user_choice -> asks user to choose a tournament
    """
    def show_message(self):
        """
        Prints message to user
        """
        print("Choisissez un tournoi parmi les suivants:")
        for id, name in tr.Tournament.available_tournaments().items():
            print(f"{id} -> {name}")

    def ask_user_choice(self):
        """
        Waiting for user's input
        """
        tournament_id = input(">>> ")
        return tournament_id


class DisplayAvailablePlayers(View):
    """
    Displays registered players not yet enlisted to tournament
    and asks user to choose one

        Attributes
        ----------
            players_list -> list of players' ids not yet enlisted
            to the tournament

        Methods
        -------
            show_message -> prints a message to user
            ask_user_choice -> asks user to choose a player
    """
    def __init__(self, players_list):
        """
        Displays registered players not yet enlisted to the tournament

            Parameters
            ----------
                players_list -> list of players' ids not yet enlisted
                to the tournament
        """
        self.players_available_ids = players_list

    def show_message(self):
        """
        Prints message to user
        """
        print("Choisissez un joueur parmi les suivants:")
        for id in self.players_available_ids:
            print(f"{id} -> "
                  f"{pl.DB.get_record_data('players',id)['first_name']} "
                  f"{pl.DB.get_record_data('players',id)['family_name']}")

    def ask_user_choice(self):
        """
        Waiting for user's input
        """
        player_id = input(">>> ")
        return player_id


class AddPlayerValidationView(View):
    """
    Displays confirmation message that player has been enlisted to tournament

        Attributes
        ----------
            player_full_name -> player's first name + family name
            tournament_name -> name of the tournament
            completed -> returns True if tournament is completed
            (default value = False)

        Methods
        -------
            show_message -> prints a message to user
            ask_user_choice -> asks user to press Enter to go back to HomePage
    """
    def __init__(self, player_full_name, tournament_name, completed=False):
        """
        Displays confirmation to user that player has been enlisted
        to tournament

            Parameters
            ----------
                player_full_name -> player's first name + family name
                tournament_name -> name of the tournament
                completed -> returns True if tournament is completed
                (default value = False)
        """
        self.player_full_name = player_full_name
        self.tournament_name = tournament_name
        self.completed = completed

    def show_message(self):
        """
        Prints message to user
        """
        print(f"{self.player_full_name} a bien été inscrit au "
              f"{self.tournament_name}.")
        if self.completed:
            print("Un round vient d'être généré pour ce tournoi.")

    def ask_user_choice(self):
        """
        Asks user to press Enter to go back to HomePage
        """
        self.back_to_homepage()
        return HomePage()


class EnterMatchScoreView(View):
    """
       Displays uncompleted tournaments and asks user to choose one

           Attributes
           ----------
                tournaments_list -> list of serialized
                tournaments that are uncompleted

           Methods
           -------
               show_message -> prints a message to user
               ask_user_choice -> asks user to choose a tournament
       """
    def __init__(self, tournaments_list=[]):
        """
        Displays list of uncompleted tournaments to user

            Parameters
            ----------
                tournaments_list -> list of serialized
                tournaments that are uncompleted
        """
        self.tournaments_list = tournaments_list

    def show_message(self):
        """
        Prints message to user
        """
        print("Choisissez un tournoi parmi les suivants:")
        for tournament in self.tournaments_list:
            print(f"{tournament['_id']} -> {tournament['name']}")

    def ask_user_choice(self):
        """
        Waiting for user's input
        """
        tournament_id = input(">>> ")
        return tournament_id


class DisplayAvailableRounds(View):
    """
       Displays uncompleted rounds and asks user to choose one

           Attributes
           ----------
                rounds_list -> list of uncompleted rounds

           Methods
           -------
               show_message -> prints a message to user
               ask_user_choice -> asks user to choose a round
       """
    def __init__(self, rounds_list=[]):
        """
        Displays uncompleted rounds to user

            Parameters
            ----------
                rounds_list -> list of uncompleted rounds

        """
        self.rounds_list = rounds_list

    def show_message(self):
        """
        Prints message to user
        """
        print("Choisissez un round parmi les suivants:")
        for round in self.rounds_list:
            print(f"{round['name'][-1]} -> {round['name']}")

    def ask_user_choice(self):
        """
        Waiting for user's input
        """
        round_id = input(">>> ")
        return round_id


class DisplayAvailableMatches(View):
    """
       Displays uncompleted matches and asks user to choose one

           Attributes
           ----------
                matches_list -> list of uncompleted matches

           Methods
           -------
               show_message -> prints a message to user
               ask_user_choice -> asks user to choose a match
       """
    def __init__(self, matches_list=[]):
        """
        Displays uncompleted matches to user

            Parameters
            ----------
                matches_list -> list of uncompleted matches

        """
        self.matches_list = matches_list

    def show_message(self):
        """
        Prints message to user
        """
        print("Choisissez un match parmi les suivants:")
        for i, match in self.matches_list:
            print(f"{i} -> {match}")

    def ask_user_choice(self):
        """
        Waiting for user's input
        """
        match_id = input(">>> ")
        return match_id


class EnterMatchScoresView(View):
    """
       Asks user to enter the score of a match

           Attributes
           ----------
                player1 -> instance of player # 1
                player2 -> instance of player # 2

           Methods
           -------
               show_message -> prints a message to user
               ask_user_choice -> asks user to enter score of the match
       """
    def __init__(self, player1, player2):
        """
           Constructor of the EnterMatchScoresView class

               Attributes
               ----------
                   player1 -> instance of player # 1
                   player2 -> instance of player # 2
           """
        self.player1 = player1
        self.player2 = player2

    def show_message(self):
        """
        Prints message to user
        """
        print(f"Entrez les scores du match {self.player1} vs "
              f"{self.player2}:")

    def ask_user_choice(self):
        """
        Waiting for user's input
        """
        score_player1 = input(f">>> Score de {self.player1}:\n")
        score_player2 = input(f">>> Score de {self.player2}:\n")
        return score_player1, score_player2


class EnterMatchScoresValidationView(View):
    """
    Displays confirmation message that match scores have been entered

        Attributes
        ----------
            round_completed -> returns True if round is completed
            (default value = False)
            tournament_completed -> returns True if tournament is completed
            (default value = False)

        Methods
        -------
            show_message -> prints a message to user
            ask_user_choice -> asks user to press Enter to go back to HomePage
    """
    def __init__(self, round_completed=False, tournament_completed=False):
        """
        Constructor of the EnterMatchScoresValidationView class

            Parameters
            ----------
                round_completed -> returns True if round is completed
                (default value = False)
                tournament_completed -> returns True if tournament is completed
                (default value = False)
        """
        self.round_completed = round_completed
        self.tournament_completed = tournament_completed

    def show_message(self):
        """
        Prints message to user
        """
        print("Le résultat du match a bien été mis à jour.")
        if self.round_completed:
            print("Le round est terminé.")
            if self.tournament_completed:
                print("Il s'agissait du dernier round, le tournoi est à "
                      "présent terminé.")
            else:
                print("Un nouveau round a été généré.")

    def ask_user_choice(self):
        """
        Asks user to press Enter to go back to HomePage
        """
        self.back_to_homepage()
        return HomePage()


class EnterPlayerRankingView(View):
    """
    Asks user to choose a player whose ranking needs to be updated

        Attributes
        ----------
            None

        Methods
        -------
            show_message -> prints a message to user
            ask_user_choice -> asks user to choose a player
    """
    def show_message(self):
        """
        Prints message to user
        """
        print("Entrez le numéro d'un des joueurs ci-dessous:\n")
        print(f"{'#':^4}{'Prénom':^20}{'Nom':^20}{'H/F':^10}"
              f"{'Classement':^10}")
        print("+" * 70)
        for player in pl.PLAYERS_TABLE:
            print(f"{player.doc_id:^4}{player['first_name']:^20}"
                  f"{player['family_name']:^20}{player['_sex']:^10}"
                  f"{player['_ranking']:^10}")
        print()

    def ask_user_choice(self):
        """
        Waiting for user's input
        """
        player_id = input(">>> ")
        return player_id


class EnterPlayerRankingValidationView(View):
    """
    Displays confirmation message that player's ranking has been updated

        Attributes
        ----------
            player_full_name -> player's first name + family name
            old_ranking -> player's previous ranking

        Methods
        -------
            show_message -> prints a message to user
            ask_user_choice -> asks user to enter new ranking
            then to press Enter to go back to HomePage
    """
    def __init__(self, player_full_name, old_ranking):
        """
        Constructor of the EnterPlayerRankingValidationView class

            Parameters
            ----------
                player_full_name -> player's first name + family name
                old_ranking -> player's previous ranking
        """
        self.player_full_name = player_full_name
        self.old_ranking = old_ranking

    def show_message(self):
        """
        Prints message to user
        """
        print(f"Entrez le nouveau classement de {self.player_full_name}:")

    def ask_user_choice(self):
        """
        Waiting for user's input
        """
        self.new_ranking = input(">>> ") or 0
        print(f"Le classement de {self.player_full_name} a été mis à jour:\n"
              f"Ancien classement -> {self.old_ranking}\n"
              f"Nouveau classement -> {self.new_ranking}")
        self.back_to_homepage()
        return self.new_ranking


class DisplayList(View):
    """
    Displays lists menu and asks user to make a choice

        Attributes
        ----------
            None

        Methods
        -------
            show_message -> prints the list of lists
            ask_user_choice -> asks user to choose a list
    """
    def show_message(self):
        """
        Prints message to user
        """
        print("Choisissez une liste parmi les suivantes:")
        self.menu = ct.LISTS_MENU
        for key in self.menu.items():
            print(key[0], ": ", key[1])

    def ask_user_choice(self):
        """
        Waiting for user's input
        """
        return input(">>> ")


class DisplayListPlayers(View):
    """
    Asks user how to sort players

        Attributes
        ----------
            None

        Methods
        -------
            show_message -> prints a message to user
            ask_user_choice -> asks user how to sort players
    """
    global SORTING_MENU

    def show_message(self):
        """
        Prints message to user
        """
        print("Classez la liste des joueurs par:")
        for element in SORTING_MENU.items():
            print(element[0], ":", element[1])
        return

    def ask_user_choice(self):
        """
        Waiting for user's input
        """
        ranking_sort = input(">>> ")
        return ranking_sort


class DisplayListPlayersResults(View):
    """
    Displays list of players

        Attributes
        ----------
            players_list -> list of players

        Methods
        -------
            show_message -> prints the list of players
            ask_user_choice -> asks user to press Enter to go back to HomePage
    """
    def __init__(self, players_list):
        """
        Constructor of the DisplayListPlayersResults class

            Parameters
            ----------
                players_list -> list of players
        """
        self.players_list = players_list

    def show_message(self):
        """
        Prints message to user
        """
        print("Voici la liste des joueurs enregistrés:\n")
        print(f"{'#':^4}{'Prénom':^20}{'Nom':^20}{'Date de Naissance':^20}"
              f"{'H/F':^6}{'Classement':^10}")
        print("+" * 80)
        for i, player in enumerate(self.players_list, start=1):
            print(f"{i:^4}{player['first_name']:^20}"
                  f"{player['family_name']:^20}"
                  f"{player['_birth_date']:^20}{player['_sex']:^6}"
                  f"{player['_ranking']:^10}")
        return

    def ask_user_choice(self):
        """
        Asks user to press Enter to go back to HomePage
        """
        self.back_to_homepage()
        return HomePage()


class DisplayListPlayersByTournament(View):
    """
    Asks user to choose a tournament

        Attributes
        ----------
            None

        Methods
        -------
            show_message -> prints a message to user
            ask_user_choice -> asks user to choose a tournament
    """
    def show_message(self):
        """
        Prints message to user
        """
        print("Choisissez un tournoi parmi les suivants:")
        for id, tournament in enumerate(tr.TOURNAMENTS_TABLE, start=1):
            print(f"{id} -> {tournament['name']}")

    def ask_user_choice(self):
        """
        Waiting for user's input
        """
        tournament_id = input(">>> ")
        return tournament_id


class DisplayListPlayersByTournamentResults(View):
    """
    Displays list of players

        Attributes
        ----------
            players_list -> list of players

        Methods
        -------
            show_message -> prints the list of players
            ask_user_choice -> asks user to press Enter to go back to HomePage
    """
    def __init__(self, players_list):
        """
        Constructor of the DisplayListPlayersByTournamentResults class

            Parameters
            ----------
                players_list -> list of players
        """
        self.players_list = players_list

    def show_message(self):
        """
        Prints message to user
        """
        print("Voici la liste des joueurs inscrits à ce tournoi:\n")
        print(f"{'#':^4}{'Prénom':^20}{'Nom':^20}{'Date de Naissance':^20}"
              f"{'H/F':^6}{'Classement':^10}")
        print("+" * 80)
        for i, player in enumerate(self.players_list, start=1):
            print(f"{i:^4}{player['first_name']:^20}"
                  f"{player['family_name']:^20}{player['_birth_date']:^20}"
                  f"{player['_sex']:^6}{player['_ranking']:^10}")
        return

    def ask_user_choice(self):
        """
        Asks user to press Enter to go back to HomePage
        """
        self.back_to_homepage()
        return HomePage()


class DisplayListTournaments(View):
    """
    A class created to keep consistency between List classes
    """
    def show_message(self):
        """
        None
        """
        pass

    def ask_user_choice(self):
        """
        None
        """
        return "0"


class DisplayListTournamentsResults(View):
    """
    Displays list of tournaments

        Attributes
        ----------
            tournaments_list -> list of tournaments

        Methods
        -------
            show_message -> prints the list of tournaments
            ask_user_choice -> asks user to press Enter to go back to HomePage
    """
    def __init__(self, tournaments_list):
        """
        Constructor of the DisplayListTournamentsResults class

            Parameters
            ----------
                tournaments_list -> list of tournaments
        """
        self.tournaments_list = tournaments_list

    def show_message(self):
        """
        Prints message to user
        """
        print("Voici la liste des tournois enregistrés:\n")
        print(f"{'#':^4}{'Nom':^20}"
              f"{'Lieu':^20}{'Date de début':^14}{'Date de fin':^14}"
              f"{'Type':^14}")
        print("+" * 86)
        for i, tournament in enumerate(self.tournaments_list, start=1):
            print(f"{i:^4}{tournament['name'][:20]:^20}"
                  f"{tournament['place']:^20}{tournament['_start_date']:^14}"
                  f"{tournament['_end_date']:^14}"
                  f"{tournament['time_control']:^14}")

    def ask_user_choice(self):
        """
        Asks user to press Enter to go back to HomePage
        """
        self.back_to_homepage()
        return HomePage()


class DisplayListRoundsByTournament(View):
    """
    Asks user to chose a tournament in order to display its rounds

        Attributes
        ----------
            None

        Methods
        -------
            show_message -> prints the list of tournaments
            ask_user_choice -> asks user to choose a tournament
    """
    def show_message(self):
        """
        Prints message to user
        """
        print("Choisissez un tournoi parmi les suivants:")
        for id, tournament in enumerate(tr.TOURNAMENTS_TABLE, start=1):
            print(f"{id} -> {tournament['name']}")

    def ask_user_choice(self):
        """
        Waiting for user's input
        """
        tournament_id = input(">>> ")
        return tournament_id


class DisplayListRoundsByTournamentResults(View):
    """
    Displays list of rounds

        Attributes
        ----------
            rounds_list -> list of tournament's rounds
            tournament_name -> name of tournament

        Methods
        -------
            show_message -> prints the list of tournament's rounds
            ask_user_choice -> asks user to press Enter to go back to HomePage
    """
    def __init__(self, rounds_list, tournament_name):
        """
        Constructor of the DisplayListRoundsByTournamentResults class

            Parameters
            ----------
                rounds_list -> list of tournament's rounds
                tournament_name -> name of tournament
        """
        self.rounds_list = rounds_list
        self.tournament_name = tournament_name

    def show_message(self):
        """
        Prints message to user
        """
        print(f"Voici la liste des rounds du {self.tournament_name}:\n")
        print(f"{'Nom':^20}{'Date de début':^20}{'Heure de début':^20}"
              f"{'Date de fin':^20}{'Heure de fin':^20}")
        print("+" * 100)
        for round in self.rounds_list:
            print(f"{round['name'][:20]:^20}{round['_start_date']:^20}"
                  f"{round['_start_time']:^20}{round['_end_date']:^20}"
                  f"{round['_end_time']:^20}")
        return

    def ask_user_choice(self):
        """
        Asks user to press Enter to go back to HomePage
        """
        self.back_to_homepage()
        return HomePage()


class DisplayListMatchesByTournament(View):
    """
    Asks user to chose a tournament in order to display its matches

        Attributes
        ----------
            None

        Methods
        -------
            show_message -> prints the list of tournaments
            ask_user_choice -> asks user to choose a tournament
    """
    def show_message(self):
        """
        Prints message to user
        """
        print("Choisissez un tournoi parmi les suivants:")
        for id, tournament in enumerate(tr.TOURNAMENTS_TABLE, start=1):
            print(f"{id} -> {tournament['name']}")

    def ask_user_choice(self):
        """
        Waiting for user's input
        """
        tournament_id = input(">>> ")
        return tournament_id


class DisplayListMatchesByTournamentResults(View):
    """
    Displays list of matches

        Attributes
        ----------
            matches_list -> list of matches
            tournament_name -> name of tournament

        Methods
        -------
            show_message -> prints the list of matches
            ask_user_choice -> asks user to press Enter to go back to HomePage
    """
    def __init__(self, matches_list, tournament_name):
        """
        Constructor of the DisplayListMatchesByTournamentResults class

            Parameters
            ----------
                matches_list -> list of matches
                tournament_name -> name of tournament
        """
        self.matches_list = matches_list
        self.tournament_name = tournament_name

    def show_message(self):
        """
        Prints message to user
        """
        print(f"Voici la liste des matchs du {self.tournament_name}:\n")
        for round, match in self.matches_list:
            print(f"{round} \n ********** \n {match} \n")

    def ask_user_choice(self):
        """
        Asks user to press Enter to go back to HomePage
        """
        self.back_to_homepage()
        return HomePage()


class DisplayListRankingsByTournament(View):
    """
    Asks user to chose a tournament in order to display its rankings

        Attributes
        ----------
            None

        Methods
        -------
            show_message -> prints the list of tournaments
            ask_user_choice -> asks user to choose a tournament
    """
    def show_message(self):
        """
        Prints message to user
        """
        print("Choisissez un tournoi parmi les suivants:")
        for id, tournament in enumerate(tr.TOURNAMENTS_TABLE, start=1):
            print(f"{id} -> {tournament['name']}")

    def ask_user_choice(self):
        """
        Waiting for user's input
        """
        tournament_id = input(">>> ")
        return tournament_id


class DisplayListRankingsByTournamentResults(View):
    """
    Displays list of players according to tournament's rankings

        Attributes
        ----------
            rankings_list -> list of players according to tournament's rankings
            tournament_name -> name of tournament
            status -> status of rankings ('définitif' or 'provisoire')
            depending on either tournament is completed or not

        Methods
        -------
            show_message -> prints the list of matches
            ask_user_choice -> asks user to press Enter to go back to HomePage
    """
    def __init__(self, rankings_list, tournament_name, status):
        """
        Constructor of the DisplayListRankingsByTournamentResults class

            Parameters
            ----------
                rankings_list -> list of players according to tournament's
                rankings
                tournament_name -> name of tournament
                status -> status of rankings ('définitif' or 'provisoire')
                depending on either tournament is completed or not
        """
        self.rankings_list = rankings_list
        self.tournament_name = tournament_name
        self.status = status

    def show_message(self):
        """
        Prints message to user
        """
        print(f"Le classement {self.status} du {self.tournament_name} "
              f"est le suivant:\n")
        print(f"{'Position':^10}{'Prénom':^20}{'Nom':^20}{'Points':^20}")
        print("+" * 70)
        for i, player in enumerate(self.rankings_list, start=1):
            print(f"{i:^10}{player['first_name']:^20}"
                  f"{player['family_name']:^20}{player['score']:^20}")

    def ask_user_choice(self):
        """
        Asks user to press Enter to go back to HomePage
        """
        self.back_to_homepage()
        return HomePage()


class ExportList(View):
    """
    A class that will use the DisplayList class to ask user to choose
    the list that needs to be exported
    """
    def show_message(self):
        """
        None
        """
        pass

    def ask_user_choice(self):
        """
        Returns a DisplayList instance
        """
        return DisplayList()


class ExportListValidation(View):
    """
    Displays a confirmation message to user that the requested list
    has been exported to a csv file

        Attributes
        ----------
            None

        Methods
        -------
            show_message -> prints a message to user
            ask_user_choice -> asks user to press Enter to go back to HomePage
    """
    def show_message(self):
        """
        Prints message to user
        """
        print("Votre liste a été exportée dans le fichier 'export.csv'.")

    def ask_user_choice(self):
        """
        Asks user to press Enter to go back to HomePage
        """
        self.back_to_homepage()
        return HomePage()


class EndPage(View):
    """
    Displays a goodbye message to user

        Attributes
        ----------
            None

        Methods
        -------
            show_message -> prints a message to user

    """
    def show_message(self):
        """
        Prints ending message to user
        """
        symbol = "+"
        message = "A bientôt !"
        print()
        print(symbol * (len(message) + 6))
        print(symbol * 2,
              f"{message.upper()}",
              symbol * 2)
        print(symbol * (len(message) + 6))
        print()
        quit()


if __name__ == "__main__":
    pass
