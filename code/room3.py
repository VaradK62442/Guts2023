from map import Map
from item import Item
from game import Game

player_pos = [5, 5]
moves = 0

key = Item("Key", "A mysterious key...", " ", [3, 4])
note = Item("Note", "A mysterious note that reads\n 'The lock must be destroyed'", "N", [4, 5])
note2 = Item("Note", "An engraving of a secret path\n 'This doesn't seem to be a lock'", "L", [4, 10])
items = [key, note,note2]
inventory = []

# 0 is open, 1 is closed (initially)
door_locations = {(2, 0): ['', 1], (9, 5): ['tutorial.pkl', 0]}

xDim = 20
yDim = 15
map = Map([xDim, yDim], door_locations)
#f = open("C:/Users/samue/OneDrive/Desktop/Hackathon/newfold/Guts2023/code/files/", "w")
with open('C:/Users/samue/OneDrive/Desktop/Hackathon/newfold/Guts2023/code/files/lock.txt', 'w') as f:
    f.write('THIS IS THE LOCK')

tutorial = Game(map, player_pos, items, inventory, key, door_locations, "room3.pkl")

tutorial.save_state("room3.pkl")