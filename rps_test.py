import rps_novo as rps

p1 = rps.Copycat_player('p1')
p2 = rps.Copycat_player('p2')
players = [p1, p2]
game = rps.Game_rounds(players, 'Jogo', 5, False)

game.play_game()

"""import turtle

t = turtle.Turtle()

t.shape('turtle')

t.goto(100,100)
t.width(10)
t.pencolor('red')
t.fillcolor('black')
t.fd(100)
t.color('blue')


import shutil
import os


columns = shutil.get_terminal_size().columns
print("hello world".center(columns))

for x in range(10):
    print(str(x).center(columns))

print(os.getcwd())



import rps_novo as rps

dictio = {'a': 2,
          'b': 1,
          'c': 3,
          'd': 4,
          'e': 5,
          'f': 6         
          }

lista = []

   
    #lista.append(dictio.popitem(max(item.values())))

def takeSecond(elem):
    return elem[1]

for item in dictio.items():
    lista.append(item)

sort = sorted(lista, reverse= True, key=takeSecond)
print(sort)




p1 = rps.Same_move_player('Non sense')
p2 = rps.Copycat_player('Rocky')

jogo = rps.Game_wins([p1,p2], "Final Game!", 5, False)

jogo.play_game()


p1 = rps.Player('p1')
p2 = rps.Player('p2')
p3 = rps.Player('p3')
p4 = rps.Player('p4')
p5 = rps.Player('p5')
p6 = rps.Player('p6')
p7 = rps.Player('p7')
p8 = rps.Human_player('p8')


players = [p1, p2, p3, p4, p5, p6, p7, p8]


champ = rps.Championship(players, "Championship")


champ.play_championship()






p = [str(x) + 'p' for x in range(1,9)]
games = {}
gamelist = []
pair_players = [[p[x],p[x+1]] for x in range(0,int(len(p)),2)]
for index in range(len(pair_players)):
    gamelist.append(rps.Game(pair_players[index]))
print(gamelist)

"""    
        
        








