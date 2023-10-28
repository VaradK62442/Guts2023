from map import Map
from item import Item
from game import Game

player_pos = [13, 5]
moves = 0

cd = Item("CD Player", "Your attention is drawn to Return of the King. When did it come out again?", "C", [1,7])
tv = Item("TV Remote", "You pick up the TV remote. The TV flickers on and asks\n 'When was paradise lost?'", "T", [4,7])
book = Item("Book", "Your attention is drawn to Paradise Lost. You pick up the book.", "B", [1,8])
# note = Item("Note", "A mysterious note that reads\n 'Welcome adventurer, we shall soon find out if you have the guts to make it through...'", "N", [4, 5])
items = [tv, cd, book]
inventory = []

# 0 is open, 1 is closed (initially)
door_locations = {(14, 10): ['level2.pkl', 1], (14, 5): ['tutorial.pkl', 0]}

xDim = 15
yDim = 15
map = Map([xDim, yDim], door_locations)

lvl = Game(map, player_pos, items, inventory, None, door_locations, "level1.pkl")

lvl.save_state("level1.pkl")