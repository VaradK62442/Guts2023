from map import Map
from item import Item
from game import Game

player_pos = [5, 5]
moves = 0

key = Item("Key", "A mysterious key...", "✠", [3, 4])
note = Item("Note", "A mysterious note that reads\n 'Welcome adventurer, we shall soon find out if you have the guts to make it through...'", "N", [4, 5])
items = [key, note]

# 0 is open, 1 is closed (initially)
door_locations = {(2, 0): ['', 1], (9, 5): ['tutorial.pkl', 0]}

xDim = 10
yDim = 15
map = Map([xDim, yDim], door_locations)

tutorial = Game(map, player_pos, items, key, door_locations, "tutorial2.pkl")

tutorial.save_state("tutorial2.pkl")