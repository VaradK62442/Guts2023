from map import Map
from item import Item
from game import Game

player_pos = [1, 2]
moves = 0

key = Item("Key", "A mysterious key...", "✠", [4, 3])
note = Item("Note", "The note reads 'fib(3)'", "N", [4, 1])

items = [key, note]
inventory = []

# 0 is open, 1 is closed (initially)
door_locations = {(0, 2): ['level1.pkl', 0], (3, 0): ['', 1], (6, 4): ['level3.pkl', 1], (9, 0): ['level4.pkl', 1], (12, 4): ['', 1], (15, 0): ['', 1]}

xDim = 25
yDim = 5
map = Map([xDim, yDim], door_locations)

lvl = Game(map, player_pos, items, inventory, key, door_locations, "level2.pkl")

lvl.save_state("level2.pkl")