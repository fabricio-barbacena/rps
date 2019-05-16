"""
    This program defines classes in order to play single games and complete
championships of Rock, Paper, Scissors between two or more players, but
always with games between two players.

    RPS stands for 'Rock, Paper, Scissors'.

    This module defines 3 classes (Player, Game and Championship) as well as
the respective Player and Game subclasses. It also defines two functions
(champ_8_players and create_players_and_play), which will be called in the
script footer.

"""

import random
import time
import string
import math
import itertools


"""
    The list below includes the three possible moves and will be used by all
the classes of players and games.
"""

moves = ['rock', 'paper', 'scissors']


class Player:
    """Define the Player class of the Rock, Paper, Scissors module.

    It is the parent class to the following subclasses:
        - Same_move_player;
        - Cyclic_player;
        - Human_player;
        - Copycat_player.

    Keyword argument:
        param(name) -- a str with the player's name.

    Instance variables:
        my_move_recorder (default: None) -- This variable will change to
            record the player's last move.
        enemy_move_recorder (default: None) -- This variable will change to
            record the opponent's last move.
    """
    def __init__(self, name):
        self.name = name
        self.my_move_recorder = None
        self.enemy_move_recorder = None

    def move(self):
        """Choose one of the three available options in the 'moves' list.

        Return a str (the value of the randomly choosen move).
        """
        my_move = random.choice(moves)
        return my_move

    def learn(self, my_move, enemy_move):
        """Inside the play_round method (from the Game class), take the
        moves of both players and register them in the respective variables.

        In this current version of the rps module, this method is built with
        the only purpose of giving the Copycat_player information to
        reproduze the oponent's last move.

        Keyword arguments:
            param1(my_move) -- the player's move in that round (a str).
            param2(enemy_move) -- the enemy's move in that round (a str).

        Return a str.
        """
        self.my_move_recorder = my_move
        self.enemy_move_recorder = enemy_move
        return self.enemy_move_recorder


class Same_move_player(Player):
    """Define a subclass of Player, which always plays the same move.

    It is the parent class of the subclass Rock_player;

    Keyword argument:
        param(name): a str with the player's name.

    Instance variable:
        my_move_recorder(str) -- set by choosing randomly one element of
            the 'moves' list, which stays the same during all the game.
            If 'rock' is chosen, this player will behave similarly to the
            Rock_player subclass.

    Inherit from the Player class:
        - the enemy_move_recorder instance variable;
        - the learn method.
    """
    def __init__(self, name):
        Player.__init__(self, name)
        self.my_move_recorder = random.choice(moves)

    def move(self):
        """Return the my_move_recorder variable"""
        return self.my_move_recorder


class Rock_player(Same_move_player):
    """A subclass of the Same_move_player subclass.

    Keyword argument:
        param(name) -- a str with the player's name.

    Instance variables:
        my_move_recorder(str) -- set to 'rock'.

    Inherit from the Player class:
        - the enemy_move_recorder instance variable;
        - the learn method.
    """
    def __init__(self, name):
        Player.__init__(self, name)
        self.my_move_recorder = 'rock'

    def move(self):
        """Return 'rock'."""
        return self.my_move_recorder


class Cyclic_player(Player):
    """Define a subclass of Player, which at first randomly chooses one move
    and then, in the next rounds, cycles through the other moves.

    Keyword argument:
        param(name) -- a str with the player's name.

    Instance variables:
        setup_executed (bool. Default: False) -- when the move method is
            called for the first time, it will also call the setup_choice
            method, and then the setup_executed variable wil change to
            True.
        my_move_recorder(str) -- set randomly when the Cyclic_player is
            created, then it will change following the patterns in the
            move method.

    Inherit from the Player class:
        - the enemy_move_recorder variable;
        - the learn method.
    """
    def __init__(self, name):
        Player.__init__(self, name)
        self.setup_executed = False
        self.my_move_recorder = random.choice(moves)

    def setup_choice(self):
        """ Change the setup_executed variable to True.

        Return the value of my_move_recorder (a str).
        """
        self.setup_executed = True
        return self.my_move_recorder

    def move(self):
        """The first time this method is called, setup_executed will still be
        False, so call the setup method.

        In the next calls of the move method, cycle through the three moves.

        Return a str.
        """
        if not self.setup_executed:
            return self.setup_choice()
        else:
            if self.my_move_recorder == 'rock':
                return 'paper'
            elif self.my_move_recorder == 'paper':
                return 'scissors'
            else:
                return 'rock'


class Human_player(Player):
    """Define a subclass of Player, where a human player inputs what moves
    she/he wants to play.

    Keyword argument:
        param(name) -- a str with the player's name.

    Inherit from the Player class:
        - the my_move_recorder instance variable;
        - the enemy_move_recorder instance variable;
        - the learn method.
    """
    def __init__(self, name):
        Player.__init__(self, name)
        self.name = name

    def move(self):
        """Ask for the Human_player's to type her/his move.

        A while loop will run as long as the input option is not in the
        'moves' list.

        Return a str with the player's move.
        """
        move = (input(f'{self.name.upper()}, time to play!\n\n'
                      '\tRock, paper, scissors? > ').
                strip(string.punctuation + ' ').lower())
        while move not in moves:
            move = (input("\tRock, paper, scissors? > ").
                    strip(string.punctuation + ' ').lower())
        self.my_move_recorder = move
        return self.my_move_recorder


class Copycat_player(Player):
    """Define a subclass of Player, which chooses a first random move and then
    copies the move played by its opponent in the previous round.

    Keyword arguments:
        param(name): a str with the player's name.

    Instance variables:
        self.first_movement (default: False) -- it will change to True
            after the move method is called for the first time.

    Inherit from the Player class:
        - the my_move_recorder variable;
        - the enemy_move_recorder variable;
        - the learn method.
    """
    def __init__(self, name):
        Player.__init__(self, name)
        self.first_movement = False

    def first_move(self):
        """Set the first_movement variable to True and choose one of the three
        elements of the 'move' list as the Copycat_player first move".
        """
        self.first_movement = True
        self.my_move_recorder = random.choice(moves)
        return self.my_move_recorder

    def move(self):
        """If first_movement == False, call the first_move method.

        If first_movement == True, copy the value of the enemy_move_recorder
        variable.

        Return a str.
        """
        if not self.first_movement:
            return self.first_move()
        else:
            move = self.enemy_move_recorder
            return move


class Game:
    """Define the basic Game class of the Rock, Paper, Scissors module.

    This is the parent class to the following subclasses:
        - Game_rounds;
        - Game_wins.

    Keyword arguments:
        param1(p) -- a list of players objects, which must have a length of 2.
            Otherwise, the check_players method will not allow the game
            to continue.
        param2(name) -- a str with the name of the game.
        param3(print_slow) -- a bool which controls the print_speed method and
            defines if the messages printed in the game will have a pause after
            it or not (Default: True).
    """
    def __init__(self, p, name, print_slow=True):
        self.p = p
        self.name = name
        self.print_slow = print_slow

    def print_speed(self, str):
        """Print a string followed by a pause of 2 seconds, if the print_slow
        variable is set to True.
        Just call the print function, if the print_slow variable is False.

        Keyword argument:
            param(str) -- the str to be printed.
        """
        if self.print_slow:
            print(str)
            time.sleep(1.25)
        else:
            print(str)

    def check_players(self):
        """Print a message and return 'not OK' if the lenght of players
        list in the game is different of 2.
        """
        if len(self.p) != 2:
            print('We need 2 players in the Game, no more, no less.\n'
                  'Please reset the game.\n')
            return 'not OK'

    def play_round(self):
        """Play a round of rps inside the game, following these steps:

        - First, play_round calls the move method for each player;
        - The players' moves are printed in a message;
        - The round_winner method is called and becomes the value for the
        winner variable;
        - The learn method is called for each player and the respective moves
        are stored in her/his/its my_move_recorder and my_enemy_recorder
        variables;
        - A message is printed, declaring the round final result.

        Return the winner variable (a str).
        """
        move1 = self.p[0].move()
        move2 = self.p[1].move()
        self.print_speed(f'\n{self.p[0].name}: {move1}, '
                         f'{self.p[1].name}: {move2}')
        winner = self.round_winner(move1, move2)
        self.p[0].learn(move1, move2)
        self.p[1].learn(move2, move1)
        if winner == 'tie':
            self.print_speed(f'\n** IT IS A TIE! **\n')
        else:
            self.print_speed(f'\n** {winner.upper()} WINS! **\n')
            return winner

    def round_winner(self, move1, move2):
        """Establish the round winner, according to standard rps rules:
            - rock beats scissors;
            - scissors beats paper;
            - paper beats rock.

        If the players play the same move, it is a tie.

        Keyword arguments:
            - param1(move1) -- the move played by the first player (a str);
            - param2(move2) -- the move played by the second player (a str);

        return:
            - the name of the player who won; or
            - the str 'tie'.
        """
        if move1 == move2:
            return 'tie'
        elif (move1 == 'rock' and move2 == 'scissors' or
              move1 == 'scissors' and move2 == 'paper' or
              move1 == 'paper' and move2 == 'rock'):
            return self.p[0].name
        else:
            return self.p[1].name

    def play_game(self):
        """Play a complete game of rps, with one round, following these steps:

            - Print the game name;
            - Print 'Game Start';
            - call the check_players method;
                - stop the game if the check_players call returns 'not OK';
            - call the play_round method;
            - print 'Game over'.
        """
        self.print_speed(f'\n{self.name.upper()}\n')
        self.print_speed('\nGame start!\n')
        number_players = self.check_players()
        if number_players == 'not OK':
            return
        else:
            self.play_round()
            self.print_speed('\nGame over!\n')


class Game_rounds(Game):
    """Define a subsclass of the Game class.

    Keyword arguments:
        param1(p) -- a list of players objects, which must have a length of 2.
            Otherwise, the check_players method will not allow the game
            to continue.
        param2(name) -- a str with the name of the game.
        param3(rounds) -- a int with the number of rounds in the Game.
        param4(print_slow) -- a bool which controls the print_speed method and
            defines if the messages printed in the game will have a pause after
            it or not (Default: True);
        param5(display_intro) -- a bool which controls whether the introduction
            method will be called or not.

    Instance variables:
        - p[0].wins -- register the first player's wins (initial value: 0);
        - p[1].wins -- register the second player's wins (initial value: 0).

    Inherit from the Game class the following methods:
        - print_speed;
        - check_players;
        - play_round;
        - round_winner.
    """
    def __init__(self, p, name, rounds, print_slow=True, display_intro=True):
        Game.__init__(self, p, name)
        self.rounds = rounds
        self.print_slow = print_slow
        self.display_intro = display_intro
        self.p[0].wins = 0
        self.p[1].wins = 0

    def introduction(self):
        """Print introductory messages, explaining how the game works."""
        if self.display_intro:
            self.print_speed(f'This game has {self.rounds} rounds.\n')
            self.print_speed('The player who has more victories after '
                             'all the rounds is the final winner!\n')
            self.print_speed('If the players have the same number of '
                             'victories by the end of the game,')
            self.print_speed('it will be declared a draw.\n\n')
        else:
            pass

    def play_game(self):
        """Play a complete game of rps, with the number of rounds defined by
        the rounds instance variable and having the following steps:

            - Print the game name and "Game Start";
            - call the check_players method;
                - stop the game if the check_players call returns 'not OK';
            - call the introduction method;
            - call the play_round method in a for loop
                    (number of loops = rounds instance variable);
                - increment one to p[0].wins or to p[1].wins
                    (depending on the round winner).
                - if there is a tie: p[0].wins and p[1].wins stay the same.
            - print 'Game over' and call the final_winner method.
        """
        self.print_speed(f'\n{self.name.upper()}\n')
        self.print_speed('\nGame start!\n')
        number_players = self.check_players()
        if number_players == 'not OK':
            return
        else:
            self.introduction()
            for round in range(self.rounds):
                self.print_speed(f'Round {str(round+1)}:\n')
                winner = self.play_round()
                print()
                if winner == self.p[0].name:
                    self.p[0].wins += 1
                elif winner == self.p[1].name:
                    self.p[1].wins += 1
                else:
                    pass
            self.print_speed('Game over!\n')
            self.final_winner()

    def final_winner(self):
        """Declare who is the final winner."""
        if self.p[0].wins > self.p[1].wins:
            self.print_speed(f'FINAL SCORE\nAFTER {self.rounds} ROUNDS:\n')
            self.print_speed(f'{self.p[0].name}: {self.p[0].wins}, '
                             f'{self.p[1].name}: {self.p[1].wins}\n\n')
            self.print_speed(f'** !!! {(self.p[0].name).upper()} '
                             f'WINS THE GAME !!! **\n')
        elif self.p[0].wins < self.p[1].wins:
            self.print_speed(f'FINAL SCORE\nAFTER {self.rounds} ROUNDS:\n')
            self.print_speed(f'{self.p[0].name}: {self.p[0].wins}, '
                             f'{self.p[1].name}: {self.p[1].wins}\n\n')
            self.print_speed(f'** !!! {(self.p[1].name).upper()} '
                             f'WINS THE GAME !!! **\n')
        else:
            self.print_speed(f'FINAL SCORE\nAFTER {self.rounds} ROUNDS:\n')
            self.print_speed(f'{self.p[0].name}: {self.p[0].wins}, '
                             f'{self.p[1].name}: {self.p[1].wins}\n\n')
            self.print_speed(f'** !!! THE GAME ENDED IN A DRAW !!! **\n')


class Game_wins(Game):
    """Define a subsclass of the Game class.

    Keyword arguments:
        param1(p) -- a list of players objects, which must have a length of 2.
            Otherwise, the check_players method will not allow the game
            to continue.
        param2(name) -- a str with the name of the game.
        param3(wins) -- a int with the round wins necessary to win the Game.
        param4(print_slow) -- a bool which controls the print_speed method and
            defines if the messages printed in the game will have a pause after
            it or not (Default: True);
        param5(display_intro) -- a bool which controls whether the introduction
            method will be called or not.

    Instance variables:
        - round -- register the number of rounds played (initial value: 1);
        - p[0].wins -- register the first player's wins (initial value: 0);
        - p[1].wins -- register the second player's wins (initial value: 0);

    Inherit from the Game class the following methods:
        - print_speed;
        - check_players;
        - play_round;
        - round_winner.
    """
    def __init__(self, p, name, wins, print_slow=True, display_intro=True):
        Game.__init__(self, p, name)
        self.wins = wins
        self.print_slow = print_slow
        self.display_intro = display_intro
        self.round = 1
        self.p[0].wins = 0
        self.p[1].wins = 0

    def introduction(self):
        """Print introductory messages, explaining how the game works."""
        if self.display_intro:
            self.print_speed(f'The player who gets {self.wins} victories '
                             'first wins the Game!\n')
            self.print_speed('There is no limit of rounds here.\n')
            self.print_speed('However, if the players keep playing the same '
                             'moves over and over again,')
            self.print_speed('the game will come to an end at the 50th '
                             'round.\n')
        else:
            pass

    def play_game(self):
        """Play a complete game of rps, with the following steps:

            - Print the Game name and "Game Start";
            - Call the check_players method;
                - Stop the game if the check_players call returns 'not OK';
            - Call the introduction method;
            - Call the play_round method in a while loop:
                - The loop will end if one of the players reaches the defined
                    number of wins;
                - The loop will break if the game reaches 50 rounds;
                - Increment one to p[0].wins or to p[1].wins in every round
                    (depending on the round winner);
                - If there is a tie in the round: p[0].wins and p[1].wins
                    stay the same;
                - Each loop increments one unit to the round instance variable;
            - Print 'Game over' and call the final_winner method;
            - Finally, p[0].wins and p[1].wins are set to 0 (so that the
                players might be used in a new game, in a Championship class).
        """
        self.print_speed(f'\n{self.name.upper()}\n')
        self.print_speed('\nGame start!\n')
        number_players = self.check_players()
        if number_players == 'not OK':
            return
        else:
            self.introduction()
            while self.p[0].wins < self.wins and self.p[1].wins < self.wins:
                if self.round > 50:
                    break
                self.print_speed(f'Round {str(self.round)}:\n')
                winner = self.play_round()
                if winner == self.p[0].name:
                    self.p[0].wins += 1
                    winner_end = self.p[0]
                elif winner == self.p[1].name:
                    self.p[1].wins += 1
                    winner_end = self.p[1]
                else:
                    pass
                self.print_speed(f'\n{self.p[0].name}: {self.p[0].wins}, '
                                 f'{self.p[1].name}: {self.p[1].wins}\n\n')
                self.round += 1
            self.print_speed('Game over!\n')
            self.final_winner()
            self.p[0].wins = 0
            self.p[1].wins = 0
            return winner_end

    def final_winner(self):
        """Declare who is the final winner."""
        if self.p[0].wins == self.wins:
            self.print_speed(f'FINAL SCORE \nAFTER {self.round-1} ROUNDS:\n')
            self.print_speed(f'{self.p[0].name}: {self.p[0].wins}, '
                             f'{self.p[1].name}: {self.p[1].wins}\n\n')
            self.print_speed(f'** !!! {(self.p[0].name).upper()} '
                             f'WINS THE GAME !!! **\n')
        elif self.p[1].wins == self.wins:
            self.print_speed(f'FINAL SCORE \nAFTER {self.round-1} ROUNDS:\n')
            self.print_speed(f'{self.p[0].name}: {self.p[0].wins}, '
                             f'{self.p[1].name}: {self.p[1].wins}\n\n')
            self.print_speed(f'** !!! {(self.p[1].name).upper()} '
                             'WINS THE GAME !!! **\n')
        else:
            self.print_speed(f'FINAL SCORE \nAFTER {self.round-1} ROUNDS:\n')
            self.print_speed(f'{self.p[0].name}: {self.p[0].wins}, '
                             f'{self.p[1].name}: {self.p[1].wins}\n\n')
            self.print_speed(f'** !!! THE GAME ENDED IN A DRAW !!! **\n')


class Championship():
    """Define a Championship Class.

    Keyword arguments:
        param1(p) -- a list of players objects, which must have a length
            equal to one of the following numbers: 2, 4, 8, 16, 32, 64, 128,
            256, 512, 1024 or 2048. Otherwise, the check_players method won't
            allow the championship to continue;
        param2(name) -- a str with the name of the championship;
        param3(first_game_intro) -- a bool which controls whether the
            introduction method of the games will be called once, in the first
            game of the championship, or not (Default: True).

    Instance variables:
        - n_phases -- a int representing the number of phases the
            championship will have;
        - print_slow -- a bool which controls the print_speed method in the
            championship objects (Default: True);
        - game.print_slow - a bool which controls the print_speed method of the
            game objects created by the set_phase method of the Championship
            Class. (Default: False);
        - players_phase -- a list of players objects. At first, it is set to
            the param1(p) of Championship. Each time the play_phase method is
            called, though, the players_phase variable is changed to a list of
            the winners of that phase (with half the lenght of the previous
            list);
        - phase_names -- initially an empty list, which will be populated by
            strings created by the name_of_phases method.
    """
    def __init__(self, p, name, first_game_intro=True):
        self.p = p
        self.name = name
        self.first_game_intro = first_game_intro
        self.n_phases = int(math.log(len(p), 2))
        self.print_slow = True
        self.game_print_slow = False
        self.game_display_intro = False
        self.players_phase = p
        self.phase_names = []

    def print_speed(self, str):
        """Print a string followed by a pause of 2 seconds, if the print_slow
        variable is set to True.
        Just call the print function, if the print_slow variable is False.

        Keyword argument:
            param(str) -- the str to be printed.
        """
        if self.print_slow:
            print(str)
            time.sleep(2)
        else:
            print(str)

    def check_players(self):
        """Print a message and return 'not OK' if the lenght of players
        list in the game is not in the following list:
            [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048].

        This list of number appears in the if statement below, as a list
        comprehension.
        """
        if len(self.p) not in [2**x for x in range(1, 12)]:
            print('\nFor this kind of Championship, we need the number of '
                  'players to be one of the following:\n\n'
                  '2, 4, 8, 16, 32, 64, 128, 256, 512, 1024 or 2048.\n\n'
                  'Please reset the game.\n')
            return 'not OK'

    def name_of_phases(self):
        """Create the phases names and append them to the phase_names list.

        Besides, depending on the length of phase_names list, add special
            nomenclatures (Final, Semi-Finals and Quarter-Finals) to the last
            three phases.
        """
        for index in range(self.n_phases):
            self.phase_names.append('Phase ' + str(index+1))
        if len(self.phase_names) == 1:
            self.phase_names[-1] += ' (Final)'
        elif len(self.phase_names) == 2:
            self.phase_names[-1] += ' (Final)'
            self.phase_names[-2] += ' (Semi-Finals)'
        else:
            self.phase_names[-1] += ' (Final)'
            self.phase_names[-2] += ' (Semi-Finals)'
            self.phase_names[-3] += ' (Quarter-Finals)'

    def set_phase(self):
        """ Set each phase of the Championship object, with these steps:

            - create an empty list called 'games';
            - create a 'pair_players' list, populated by lists with two players
                each, players taken from the players_phase list. Thus,
                pair_players will have half the length of players_phase;
            - a for loop will loop over each list of two players, in the
                pair_players list, and use these pair of players to create
                Game_wins objects and append them to the games list;
            - the if/else statements are structured in this method to determine
                whether the first game of the championship will display an
                introduction (if statement part, when first_game_intro is True)
                or not (the else part).

            Return the games list.
        """
        self.games = []
        self.pair_players = [[self.players_phase[x], self.players_phase[x+1]]
                             for x in range(0, len(self.players_phase), 2)]
        if self.first_game_intro:
            self.first_game_intro = False
            game_name = 'Game ' + str(1)
            self.game_display_intro = True
            self.games.append(Game_wins(self.pair_players[0], game_name,
                                        3, self.game_print_slow,
                                        self.game_display_intro))
            self.game_display_intro = False
            for index in range(len(self.pair_players)-1):
                game_name = 'Game ' + str(index+2)
                self.games.append(Game_wins(self.pair_players[index+1],
                                            game_name, 3, self.game_print_slow,
                                            self.game_display_intro))
        else:
            self.game_display_intro = False
            for index in range(len(self.pair_players)):
                game_name = 'Game ' + str(index+1)
                self.games.append(Game_wins(self.pair_players[index],
                                            game_name,
                                            3,
                                            self.game_print_slow,
                                            self.game_display_intro))
        return self.games

    def play_phase(self):
        """ Play a complete phase of the Championship, following these steps:

            - the set_phase method is called and the returned list is stored
                in the games variable;
            - an empty winners list is created;
            - a for loop will loop over each game in the games list:
                - the play_game method of the game object is called and the
                    winner player object is appended to the winners list;
            - when the loop is done, the Championship players_phase instance
                    variable is changed to the value stored here in the
                    winners list;
        """
        self.games = self.set_phase()
        self.winners = []
        for game in self.games:
            winner = game.play_game()
            self.winners.append(winner)
        self.players_phase = self.winners

    def play_championship(self):
        """ Play a complete championship of rps, with the following steps:

            - print a welcome message;
            - call the check_players method and interrupt the championship if
                the number of players is "not OK";
            - call the name_of_phases method;
            - use a for loop to:
                - print the phase name;
                - call the play_phase method for that phase;
            - call the declare_champion method, when the championship is done
                playing the last phase.
        """
        self.print_speed(f'\nWelcome to the {self.name.upper()}')
        check_players = self.check_players()
        if check_players == 'not OK':
            return
        self.name_of_phases()
        for phase in range(self.n_phases):
            self.print_speed(f'\n{self.phase_names[phase].upper()}')
            self.play_phase()
        self.declare_champion()

    def declare_champion(self):
        """ Print messages declaring the final champion of the Championship."""
        self.print_speed(f'End of the {self.name}!\n')
        self.print_speed('The final champion is')
        self.print_speed(f'\n** {self.players_phase[0].name} **\n')
        self.print_speed('CONGRATULATIONS, '
                         f'{self.players_phase[0].name.upper()}!\n')


def champ_8_players():
    """Play a Championship with 8 players (all players subclasses included)"""
    your_name = input('Enter your name: ')

    human = Human_player(your_name)
    same = Same_move_player('Same Move')
    cyclic = Cyclic_player('Cyclic')
    rock = Rock_player('Rock Player')
    random1 = Player('Ann (Random)')
    random2 = Player('Alf (Random)')
    random3 = Player('John (Random)')
    copycat = Copycat_player('Copycat')

    players = [human, same, cyclic, rock, random1, random2, random3, copycat]

    champ = Championship(players, "\n\n** !!!REWIEWER'S CUP!!! **")
    champ.print_slow = True
    champ.game_print_slow = True

    champ.play_championship()


def create_players_and_play():
    "Create 2047 Player objects and one Player_human, and make them play!"
    your_name = input('Enter your name: ')
    number_of_players = 2048
    players = []
    for n in range(number_of_players - 1):
        players.append(Player('Player ' + str(n+1)))
    players.append(Human_player(your_name))
    champ = Championship(players, '2048 CUP!')
    if number_of_players > 8:
        champ.print_slow = True
        champ.game_print_slow = False
    champ.play_championship()


if __name__ == '__main__':
    champ_8_players()
    print('Dear Reviewer, prepare to be amazed by the thousands of RPS games '
          'being played in front of you!')
    time.sleep(3.5)
    print('Your human player will play at first in the Game 1024')
    time.sleep(1)
    print("Ready??? Let's go!\n")
    create_players_and_play()
