from map import Map
from item import Item
from game import Game

player_pos = [5, 19]
moves = 0

tv = Item("TV Remote", "You pick up the TV remote. The TV flickers on and asks\n 'Where did the eagles not dare in 2003?'", "T", [5, 5])

items = [tv]
inventory = []

# 0 is open, 1 is closed (initially)
door_locations = {(5, 19): ['level2.pkl', 0]}

xDim = 10
yDim = 20
map = Map([xDim, yDim], door_locations)

lvl = Game(map, player_pos, items, inventory, None, door_locations, "level3.pkl")

lvl.save_state("level3.pkl")