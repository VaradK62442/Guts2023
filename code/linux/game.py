import tkinter as tk
import pygame
import random
import pickle

import os
from screeninfo import get_monitors

from item import Item
from map import Map


class Game(tk.Tk):
    def __init__(self, map, player_pos, items, inventory, key, door_locations, filename):
        super().__init__()
        self.title("Halloween Escape Room")
        for m in get_monitors():
            width = m.width
            height = m.height

        # width = self.winfo_screenwidth()
        # height = self.winfo_screenheight()

        self.geometry(f"{width}x{height}")
        self.configure(bg="black")

        pygame.mixer.init()

        self.filename = filename

        self.tvAnswerCorrect = False

        # Ensure the path to the Music.mp3 file is correct
        pygame.mixer.music.load("./files/Music.mp3")
        pygame.mixer.music.play(-1)

        self.map = map

        self.player_pos = player_pos
        self.map.add_to_map("⯌", self.player_pos)
        self.moves = 0

        self.firstTimeL2 = True

        self.inLevel1, self.inLevel3 = False, False

        # self.key = Item("Key", "A mysterious key...", "✠", [7, 7])
        # self.map.add_to_map(self.key, self.key.position)

        # self.note = Item("Note", "A mysterious note that reads\n 'Welcome adventurer, we shall soon find out if you have the guts to make it through...'", "N", [2, 2])
        # self.map.add_to_map(self.note, self.note.position)

        self.items = items
        self.inventory = inventory

        # add everything to map
        for item in items:
            self.map.add_to_map(item, item.position)

        self.key = key
        self.door_locations = door_locations

        self.canvas = tk.Canvas(self, width=1000, height=500, bg="black")
        self.canvas.pack()

        self.message_label = tk.Label(
            self, text="", bg="black", fg="white", font=("Arial", 10))
        self.message_label.pack(side="bottom")

        self.position_label = tk.Label(
            self, text=f"Player Position: {self.player_pos}", bg="black", fg="white", font=("Arial", 10))
        self.position_label.pack(side="left")

        self.inventory_label = tk.Label(
            self, text="Inventory: ", bg="black", fg="white", font=("Arial", 10))
        self.inventory_label.pack(side="right")

        self.controls_label = tk.Label(
            self, text="Controls: W, A, S, D to move; E to interact; Q to quit", bg="black", fg="white", font=("Arial", 10))
        self.controls_label.pack(side="top")

        self.bind("<Key>", self.key_press)
        # bind the "i" key to show inventory
        self.bind("<i>", self.show_inventory)

        self.update_map()

    def show_inventory(self, event=None):
        if not self.winfo_exists():  # Check if the window exists
            return

        popup = tk.Toplevel(self)
        popup.title("Inventory")

        for item in self.inventory:
            label = tk.Label(
                popup, text=f"{item.name}: {item.description}", wraplength=300, font=("Arial", 10))
            label.pack(pady=5, padx=5)

        tk.Button(popup, text="Close", command=popup.destroy).pack(pady=5)

    def tvRemoteAnswer(self):
        print(self.entry.get())
        if self.inLevel3:
            if self.entry.get().lower() == "mordor":
                self.tvAnswerCorrect = True
                self.popup.destroy()
        elif self.inLevel1:
            if self.entry.get() == "1667":
                self.tvAnswerCorrect = True
                self.popup.destroy()

    def check_file(self, file_name):
        files = os.listdir("./files/")
        if file_name in files:
            return True
        else:
            return False

    def create_popup(self, item):

        if item.name == "TV Remote":
            if self.filename == "level1.pkl":
                self.inLevel1 = True

                self.popup = tk.Toplevel(self)
                self.popup.title(item.name)

                label = tk.Label(self.popup, text=item.description,
                                 wraplength=300, font=("Chiller", 20))
                label.pack(pady=20, padx=20)

                self.entry = tk.Entry(
                    self.popup, text="", font=("Chiller", 20))
                self.entry.pack(pady=20, padx=20)

                tk.Button(self.popup, text="Enter", width=20,
                          command=self.tvRemoteAnswer).pack(pady=20)
            elif self.filename == "level3.pkl":
                self.inLevel3 = True

                self.popup = tk.Toplevel(self)
                self.popup.title(item.name)

                label = tk.Label(self.popup, text=item.description,
                                 wraplength=300, font=("Chiller", 20))
                label.pack(pady=20, padx=20)

                self.entry = tk.Entry(
                    self.popup, text="", font=("Chiller", 20))
                self.entry.pack(pady=20, padx=20)

                tk.Button(self.popup, text="Enter", width=20,
                          command=self.tvRemoteAnswer).pack(pady=20)

        elif item.name not in ["Key"]:
            popup = tk.Toplevel(self)
            popup.title(item.name)

            label = tk.Label(popup, text=item.description,
                             wraplength=300, font=("Chiller", 20))
            label.pack(pady=20, padx=20)

    def update_inventory_label(self):
        inventory_text = "Inventory: " + \
            ", ".join([item.name for item in self.inventory])
        self.inventory_label.config(text=inventory_text)

    def display_message(self, mssg):
        self.message_label.config(text=mssg)

    def update_map(self):
        self.map.show_map(self.canvas)

    def display_win_message(self):
        popup = tk.Toplevel(self)
        popup.title("Congratulations!")
        label = tk.Label(
            popup, text="Your soul is safe for another day", font=("Chiller", 20))
        label.pack(pady=20, padx=20)

    def check_key(self, new_pos):
        message = None
        if self.key not in self.inventory and self.door_locations[tuple(new_pos)][1] == 1:
            message = "The door is locked. You need a key to unlock it."
        elif self.door_locations[tuple(new_pos)][1] == 0:
            # Clear current player position
            self.map.add_to_map(".", self.player_pos)
            self.player_pos = new_pos
            # Add player to new position
            self.map.add_to_map("⯌", self.player_pos)
            self.moves += 1
        elif self.key in self.inventory:
            self.door_locations[tuple(new_pos)][1] = 0
            self.inventory.remove(self.key)  # remove key if used on door
            self.update_inventory_label()
            # Clear current player position
            self.map.add_to_map(".", self.player_pos)
            self.player_pos = new_pos
            # Add player to new position
            self.map.add_to_map("⯌", self.player_pos)
            self.moves += 1
        return message

    def key_press(self, event):
        if not self.winfo_exists():  # Check if the window exists
            return

        self.update_inventory_label()

        message = ""
        if event.keysym in ['w', 'a', 's', 'd']:
            new_pos = self.player_pos.copy()
            if event.keysym == 'w' and new_pos[1] > 0:
                new_pos[1] -= 1
            elif event.keysym == 's' and new_pos[1] < self.map.dimen[1] - 1:
                new_pos[1] += 1
            elif event.keysym == 'a' and new_pos[0] > 0:
                new_pos[0] -= 1
            elif event.keysym == 'd' and new_pos[0] < self.map.dimen[0] - 1:
                new_pos[0] += 1

            if self.player_pos == [9, 0]:
                print("Setting first time to false")
                self.firstTimeL2 = False
                print(f"first time val: {self.firstTimeL2}")

            if self.tvAnswerCorrect:
                key = Item("Key", "A mysterious key...", "✠", [7, 7])
                self.inventory.append(key)
                self.key = key
                self.tvAnswerCorrect = False

            for item in self.inventory:
                if item.name == "Key":
                    self.key = item

            # Check if the new position contains an item or other impassable object
            if self.map.arr[new_pos[1]][new_pos[0]] not in ['D', '|', '-'] + [item.representation for item in self.items] or tuple(new_pos) in self.door_locations:
                if tuple(new_pos) in self.door_locations:
                    #!!!!!!!!!!!!!!!!!!!!!!!!!!
                    # Here i kept the condition cheking, but the code inside each codition check is the same,
                    # also, now i got it so you can go back to every room, including the 2nd tv one
                    if self.filename[0] == "r":
                        # message = self.check_key(new_pos)
                        # if message != None:  # just for the special message of this room
                        #     message = "The door is locked. You need to do something to the lock."
                        if self.check_file("lock.txt") and self.door_locations[tuple(new_pos)][1] == 1:
                            message = "The door is locked. You need to do something to the lock."
                        else:
                            self.door_locations[tuple(new_pos)][1] = 0
                            self.map.add_to_map(".", self.player_pos)  # Clear current player position
                            self.player_pos = new_pos
                            self.map.add_to_map("⯌", self.player_pos)  # Add player to new position
                            self.moves += 1
                    elif self.filename == "level2.pkl":
                        if new_pos == [9, 0] and self.firstTimeL2 == True:
                            # if self.key not in self.inventory and self.door_locations[tuple(new_pos)][1] == 1:
                            #   message = "The door is locked. You need a key to unlock it."
                            # elif self.key in self.inventory:
                            #   self.door_locations[tuple(new_pos)][1] = 0
                            #  self.inventory.remove(self.key) # remove key if used on door
                            # self.update_inventory_label()
                            # self.map.add_to_map(".", self.player_pos)  # Clear current player position
                            #    self.player_pos = new_pos
                            #   self.map.add_to_map("⯌", self.player_pos)  # Add player to new position
                            #  self.moves += 1
                            message = self.check_key(new_pos)
                        elif new_pos == [6, 4] and self.firstTimeL2 == False:
                            #            if self.key not in self.inventory and self.door_locations[tuple(new_pos)][1] == 1:
                            #            message = "The door is locked. You need a key to unlock it."
                            #        elif self.key in self.inventory:
                            #            self.door_locations[tuple(new_pos)][1] = 0
                            #            self.inventory.remove(self.key) # remove key if used on door
                            #        self.update_inventory_label()
                            #        self.map.add_to_map(".", self.player_pos)  # Clear current player position
                            #        self.player_pos = new_pos
                            #        self.map.add_to_map("⯌", self.player_pos)  # Add player to new position
                            #    self.moves += 1
                            message = self.check_key(new_pos)
                        elif self.door_locations[tuple(new_pos)][1] == 0:
                            # Clear current player position
                            self.map.add_to_map(".", self.player_pos)
                            self.player_pos = new_pos
                            # Add player to new position
                            self.map.add_to_map("⯌", self.player_pos)
                            self.moves += 1
                        else:
                            message = "The door is locked. You need a key to unlock it."

                    else:
                        message = self.check_key(new_pos)
                else:
                    # Clear current player position
                    self.map.add_to_map(".", self.player_pos)
                    self.player_pos = new_pos
                    # Add player to new position
                    self.map.add_to_map("⯌", self.player_pos)
                    self.moves += 1

        if event.keysym == 'e':
            for item in self.items:
                if abs(self.player_pos[0] - item.position[0]) <= 1 and abs(self.player_pos[1] - item.position[1]) <= 1:
                    if item not in self.inventory:
                        self.inventory.append(item)
                        self.items.remove(item)
                        self.update_inventory_label()
                        self.create_popup(item)
                        # Remove item representation from the map after it's collected
                        print(item.position)
                        self.map.add_to_map(".", item.position)
                        break

            # if player opens door and leaves
            # and self.key in self.inventory:
            if tuple(self.player_pos) in self.door_locations:
                self.save_state(self.filename)
                pp = tuple(self.player_pos)
                dl = self.door_locations
                inv = self.inventory
                self.destroy()

                load_state(dl[pp][0], inv)

        elif event.keysym == 'q':
            self.destroy()

        self.message_label.config(fg="white")

        self.update_map()

        self.position_label.config(text=f"Player Position: {self.player_pos}")

        if message != None:
            self.display_message(message)

    def save_state(game, filename):
        game_info = ["title", "geom", game.map, game.player_pos,
                     game.items, game.inventory, game.key, game.door_locations]
        pickle.dump(game_info, open('./levels/' + filename, "wb"))


def load_state(filename, inv=[]):
    print("Trying to load ", filename)
    me = pickle.load(open("./levels/" + filename, "rb"))
    me = Game(me[2], me[3], me[4], inv, me[6], me[7], filename)
    me.mainloop()


if __name__ == "__main__":
    # pickle everything
    level_names = ['tutorial', 'level1', 'level2', 'level3', 'room3', 'win']
    for level in level_names:
        os.system(f'python3 {level}.py')

    load_state(level_names[0] + '.pkl', [])
    # load_state("level2.pkl")
