from map import Map
from item import Item
from game import Game

player_pos = [5, 5]
moves = 0

key = Item("Key", "A mysterious key...", "✠", [7, 7])
note = Item("Note", "A mysterious note that reads\n 'Welcome adventurer, we shall soon find out if you have the guts to make it through...'", "N", [2, 2])
items = [key, note]

door_locations = [[0, 6]]

xDim = 15
yDim = 10
map = Map([xDim, yDim], door_locations)

tutorial = Game(map, player_pos, items, key, door_locations)

tutorial.save_state("tutorial.pkl")