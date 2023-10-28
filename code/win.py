from map import Map
from item import Item
from game import Game

player_pos = [9, 1]
moves = 0

note = Item("Note", "Well well well...\nIt appears you did have the guts...\nCongratulations for completing the escape room. You have proven your skill.", "N", [4, 5])
items = [note]
inventory = []

# 0 is open, 1 is closed (initially)
door_locations = {(9, 0): ['room3.pkl', 0]}

xDim = 30
yDim = 30
map = Map([xDim, yDim], door_locations)

tutorial = Game(map, player_pos, items, inventory, None, door_locations, "win.pkl")

tutorial.save_state("win.pkl")