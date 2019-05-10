import random
import time
import string
import math
import itertools
import pprint

"""
    This program defines objects to play games and championships of Rock, Paper,
Scissors between two players or more players, but always placed in games
between two players.

    RPS stands for 'rock-paper-scissors'

    The list below includes the three possible moves, and will be used by all
the classes of players and games.
"""

moves = ['rock', 'paper', 'scissors']

""""""


class Player:
    def __init__(self, name):
        """
        Define the Player class of the rock-paper-scissors module.

        Arg:
            param1 (name): a str with the player's name.

        Attributes:
            my_move_recorder: initial value is None. It will change to record
                the player's last move.
            enemy_move_recorder: initial value is None. It will change to
                record the oponent's last move.
        """
        self.name = name
        self.my_move_recorder = None
        self.enemy_move_recorder = None

    def move(self):
        """
        Choose randomly one of the three option available in the 'moves' list
        and set it as the new value of my_move_recorder.
        
        Return (str):
            The value of choosen move.
        """
        my_move = moves[(random.randint(0,2))]
        return my_move

    def learn(self, my_move, enemy_move):
        """
        Inside the play_round method (from the Game class), take the
        moves of both players and register in the respective variables.

        In this current version of the module, this method is built with
        the only purpose of giving the Copycat_player information to
        reproduze the oponent's moves.

        Arg:
            param1 (str) = the player's move, played in that round.
            param2 (str) = the enemy's move, played in that round.

        Return: (str)
            
        """
        self.my_move_recorder = my_move
        self.enemy_move_recorder = enemy_move
        return self.enemy_move_recorder


class Same_move_player(Player):
    def __init__(self, name):
        """
        Define a subclass of Player, which always plays the same move.

        Arg:
            param(name): a str with the player's name.

        Attributes:
            my_move_recorder(str): set by choosing randomly one element of
                the 'moves' list, which stays the same during all the game.

        Inherit from the Player class:
            - the enemy_move_recorder attribute
            - the learn method
        """
        Player.__init__(self, name)
        self.my_move_recorder = random.choice(moves)

    def move(self):
        """Return the player's move set when he was created."""
        return self.my_move_recorder


class Rock_player(Same_move_player):
        """
        A subclass of the Same_move_player subclass.

        Arg:
            param(name): a str with the player's name.

        Attributes:
            my_move_recorder(str): set to 'rock'.

        Inherit from the Player class:
            - the enemy_move_recorder attribute
            - the learn method
        """
    def __init__(self, name):
        Player.__init__(self, name)
        self.my_move_recorder = 'rock'

    def move(self):
        """return 'rock' all the times"""
        return self.my_move_recorder


class Cyclic_player(Player):
    def __init__(self, name):
        Player.__init__(self, name)
        self.setup_executed = False
        self.my_move_recorder = random.choice(moves)

    def setup_choice(self):
        self.setup_executed = True
        return self.my_move_recorder

    def move(self):
        if self.setup_executed == False:
            self.setup_choice()
        else:
            if self.my_move_recorder == 'rock':
                return 'paper'
            elif self.my_move_recorder == 'paper':
                return 'scissors'
            else:
                return 'rock'


class Human_player(Player):
    def __init__(self, name=None):
        Player.__init__(self, name)
        self.name = input("\nWhat player's name do you choose for yourself? ")

    def move(self):
        move = (input(f'{self.name.upper()}, time to play!\n\n'
                      '\tRock, paper, scissors? > ').
                strip(string.punctuation + ' ').lower())
        while move not in moves:
            """if move in ['quit', 'exit', 'leave']:
                print('\n leaving the game...\n...\n')
                break"""
            move = (input("\tRock, paper, scissors? > ").
                    strip(string.punctuation + ' ').lower())
        self.my_move_recorder = move
        return self.my_move_recorder


class Copycat_player(Player):
    def __init__(self, name):
        Player.__init__(self, name)
        self.first_movement = False
        self.my_move_recorder = None
        self.enemy_move_recorder = None

    def first_move(self):
        self.first_movement = True
        self.my_move_recorder = random.choice(moves)
        return self.my_move_recorder

    def move(self):
        if self.first_movement == False:
            return self.first_move()
        else:
            move = self.enemy_move_recorder
            return move


class Game:
    def __init__(self, p, name, print_slow=True):
        self.p = p
        self.name = name
        self.print_slow = print_slow 

    def print_speed(self, str):
        if self.print_slow == True:
            print(str)
            time.sleep(2)
        else:
            print(str)

    def check_players(self):
        if len(self.p) != 2:
            print('We need 2 players in the Game, no more, no less.\n'
                  'Please reset the game.\n')
            return 'not OK'


    def play_round(self):
        move1 = self.p[0].move()
        move2 = self.p[1].move()
        self.print_speed(f'\n{self.p[0].name}: {move1}  '
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
        if move1 == move2:
            return 'tie'
        elif (move1 == 'rock' and move2 == 'scissors' or
              move1 == 'scissors'and move2 == 'paper' or
              move1 == 'paper'and move2 == 'rock'):
            return self.p[0].name
        else:
            return self.p[1].name

    def play_game(self):
        self.print_speed(f'\n{self.name.upper()}\n')
        self.print_speed('\nGame start!\n')
        number_players = self.check_players()
        if number_players == 'not OK':
            return
        else:
            self.play_round()
            print()
            self.print_speed('Game over!\n')


class Game_rounds(Game):
    def __init__(self, p, name, rounds, print_slow=True):
        Game.__init__(self, p, name)
        self.rounds = rounds
        self.print_slow = print_slow
        self.p[0].wins = 0
        self.p[1].wins = 0

    def introduction(self):
        self.print_speed(f'This game has {self.rounds} rounds.\n')
        self.print_speed('The player who has more victories after '
                         'all the rounds is the final winner!\n')
        self.print_speed('If the players have the same number of victories '
                         'by the end of the game,')
        self.print_speed('it will be declared a draw.\n\n')

    def play_game(self):
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
    def __init__(self, p, name, wins, print_slow=True ):
        Game.__init__(self, p, name)
        self.wins = wins
        self.print_slow = print_slow
        self.round = 1
        self.p[0].wins = 0
        self.p[1].wins = 0

    def introduction(self):
        self.print_speed(f'The player who gets {self.wins} victories first '
                         'wins the Game!\n')
        self.print_speed('There is no limit of rounds here.\n')
        self.print_speed('However, if the players keep playing the same moves '
                         'over and over again, the game will come to an end '
                         'at the 50th round.\n')

    def play_game(self):
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
                print()
                if winner == self.p[0].name:
                    self.p[0].wins += 1
                    winner_end = self.p[0]
                elif winner == self.p[1].name:
                    self.p[1].wins += 1
                    winner_end = self.p[1]
                else:
                    pass
                self.print_speed(f'{self.p[0].name}: {self.p[0].wins}, '
                                 f'{self.p[1].name}: {self.p[1].wins}\n\n')
                self.round += 1
            self.print_speed('Game over!\n')
            self.final_winner()
            self.p[0].wins = 0
            self.p[1].wins = 0
            return winner_end


    def final_winner(self):
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
    def __init__(self, p, name):
        self.p = p
        self.name = name
        self.n_phases = int(math.log(len(p), 2))
        self.print_slow = True
        self.game_print_slow = True
        self.players_phase = p
        self.phase_names = []

    def print_speed(self, str):
        if self.print_slow == True:
            print(str)
            time.sleep(2)
        else:
            print(str)

    def check_players(self):
        if len(self.p) not in [2**x for x in range(1,12)]:
            print('\nFor this kind of Championship, we need the number of '
                  'players to be one of the following:\n\n'
                  '2, 4, 8, 16, 32, 64, 128, 256, 512, 1024 or 2048.\n\n'
                  'Please reset the game.\n')
            return 'not OK'

    def name_of_phases(self):
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
        self.games = []
        self.pair_players = [[self.players_phase[x],self.players_phase[x+1]]
                             for x in range(0,int(len(self.players_phase)),2)]
        for index in range(len(self.pair_players)):
            name = 'Game ' + str(index+1)
            self.games.append(Game_wins(self.pair_players[index], name,
                                        3, self.game_print_slow))
        return self.games

    def play_phase(self):
        self.games = self.set_phase()
        self.winners = []
        for game in self.games:
            winner = game.play_game()
            self.winners.append(winner)
        self.players_phase = self.winners

    def play_championship(self):
        check_players = self.check_players()
        if check_players == 'not OK':
            return
        self.name_of_phases()
        for phase in range(self.n_phases):
            self.print_speed(f'\n{self.phase_names[phase].upper()}')
            self.play_phase()
        self.declare_champion()

    def declare_champion(self):
        self.print_speed(f'End of the {self.name}!\n')
        self.print_speed('The final champion is')
        self.print_speed(f'\n** {self.players_phase[0].name}**\n')
        self.print_speed('CONGRATULATIONS, '
                         f'{self.players_phase[0].name.upper()}!\n') 


class Championship_points(Championship):
    def __init__(self, p, name):
        Championship.__init__(self, p, name)
        self.print_slow = True
        self.game_print_slow = True
        self.points = {}
        self.players_pairs = []
        self.games = []

    def print_speed(self, str):
        if self.print_slow == True:
            print(str)
            time.sleep(2)
        else:
            print(str)

    def set_players_in_game(self):
        self.players_pairs = list(itertools.combinations(self.p, 2))
        pprint.pprint(self.players_pairs)
        for player in self.p:
            self.points.setdefault(player.name, 0)

    def set_games(self):
        for pair in self.players_pairs:
            self.games.append(Game_wins(pair, 'Game ' +
                                          str(self.players_pairs.index(pair)+1),
                                          3, self.game_print_slow))

    def play_championship(self):
        points = self.points
        self.set_players_in_game()
        self.set_games()
        for game in self.games:
            winner = game.play_game()
            points[winner.name] += 1
            self.sorting_wins
        self.points = points
        self.sorting_wins()

    def sorting_wins(self):
        final = sorted(self.points.items(), reverse=True,
                       key = lambda kv:(kv[1], kv[0]))
        print()
        print(final)




if __name__ == '__main__':
    p1 = Player('p1')
    p2 = Player('p2')
    p3 = Player('p3')
    p4 = Human_player('p4')

    players = [p1, p2, p3, p4]

    champ = Championship_points(players, 'Champ')

    champ.play_championship()



"""
if __name__ == '__main__':
    number_of_players = 4
    players = []
    for n in range(number_of_players - 1):
        players.append(Player('Player ' + str(n+1)))
    players.append(Human_player())
    champ = Championship(players, 'Championship')
    if number_of_players > 32:
        champ.print_slow = False
        champ.game_print_slow = False
    champ.play_championship()
"""

