import tkinter as tk
import pygame
import random
import pickle

from item import Item
from map import Map

class Game(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Halloween Escape Room")
        self.geometry("420x420")
        self.configure(bg="black")

        pygame.mixer.init()
        
        # Ensure the path to the Music.mp3 file is correct
        pygame.mixer.music.load("./code/files/Music.mp3")
        pygame.mixer.music.play(-1)

        self.map = Map([10, 10])

        self.player_pos = [5, 5]
        self.map.add_to_map("⯌", self.player_pos)
        self.moves = 0

        self.key = Item("Key", "A mysterious key...", "✠", [7, 7])
        self.map.add_to_map(self.key, self.key.position)

        self.note = Item("Note", "A mysterious note that reads\n 'Welcome adventurer, we shall soon find out if you have the guts to make it through...'", "N", [2, 2])
        self.map.add_to_map(self.note, self.note.position)

        self.items = [self.key, self.note]
        self.inventory = []

        self.canvas = tk.Canvas(self, width=400, height=300, bg="black")
        self.canvas.pack()

        self.message_label = tk.Label(self, text="", bg="black", fg="white", font=("Arial", 10))
        self.message_label.pack(side="bottom")

        self.position_label = tk.Label(self, text=f"Player Position: {self.player_pos}", bg="black", fg="white", font=("Arial", 10))
        self.position_label.pack(side="left")

        self.inventory_label = tk.Label(self, text="Inventory: ", bg="black", fg="white", font=("Arial", 10))
        self.inventory_label.pack(side="right")

        self.controls_label = tk.Label(self, text="Controls: W, A, S, D to move; E to interact; Q to quit", bg="black", fg="white", font=("Arial", 10))
        self.controls_label.pack(side="top")
        
        self.bind("<Key>", self.key_press)

        self.update_map()
    
    def create_popup(self, item):
        
        # if item.name == "Key":
        #     canvas = tk.Canvas(popup, width=100, height=100, bg="white")
        #     canvas.pack()
        #     self.draw_key(canvas)
            
        if item.name == "Note":
            popup = tk.Toplevel(self)
            popup.title(item.name)

            label = tk.Label(popup, text=item.description, wraplength=300, font=("Chiller", 20))
            label.pack(pady=20, padx=20)

    def draw_key(self, canvas):
        colors = ["yellow", "brown"]
        key_pixels = [
            " 0011 ",
            " 0011 ",
            "111111",
            "  11  ",
            "  11  ",
        ]
        self.draw_pixels(canvas, key_pixels, colors)

    def draw_book(self, canvas):
        colors = ["blue", "white"]
        book_pixels = [
            "11111",
            "10001",
            "10001",
            "10001",
            "11111",
        ]
        self.draw_pixels(canvas, book_pixels, colors)

    def draw_pixels(self, canvas, pixels, colors):
        for y, row in enumerate(pixels):
            for x, char in enumerate(row):
                if char != " ":
                    color = colors[int(char)]
                    canvas.create_rectangle(x * 10, y * 10, (x + 1) * 10, (y + 1) * 10, fill=color, outline=color)


    def update_inventory_label(self):
        inventory_text = "Inventory: " + ", ".join([item.name for item in self.inventory])
        self.inventory_label.config(text=inventory_text)

    def display_message(self,mssg):
        self.message_label.config(text = mssg)

    def update_map(self):
        self.map.show_map(self.canvas)

    def display_win_message(self):
        popup = tk.Toplevel(self)
        popup.title("Congratulations!")
        label = tk.Label(popup, text="Your soul is safe for another day", font=("Chiller", 20))
        label.pack(pady=20, padx=20)

    def key_press(self, event):
        if not self.winfo_exists():  # Check if the window exists
            return
        
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

            # Check if the new position contains an item or other impassable object
            if self.map.arr[new_pos[1]][new_pos[0]] not in ['D', 'N', '✠', '|', '-'] or new_pos == [0, 5]:
                if new_pos == [0, 5] and self.key not in self.inventory:
                    message = "The door is locked. You need a key to unlock it."
                else:
                    self.map.add_to_map(".", self.player_pos)  # Clear current player position
                    self.player_pos = new_pos
                    self.map.add_to_map("⯌", self.player_pos)  # Add player to new position
                    self.moves += 1

        self.key.representation = "✠" # if self.moves % 2 == 0 else "✠"

        if event.keysym == 'e':
            for item in self.items:
                if abs(self.player_pos[0] - item.position[0]) <= 1 and abs(self.player_pos[1] - item.position[1]) <= 1:
                    if item not in self.inventory:
                        self.inventory.append(item)
                        self.items.remove(item)
                        self.update_inventory_label()
                        self.create_popup(item)
                        # Remove item representation from the map after it's collected
                        self.map.add_to_map(".", item.position)
                        break

            if self.player_pos == [0, 5] and self.key in self.inventory:
                pygame.mixer.music.stop()
                self.display_win_message()
                self.unbind("<Key>")
                return
        
        elif event.keysym == 'q':
            self.destroy()

        self.message_label.config(fg="white")

        self.update_map()

        self.position_label.config(text=f"Player Position: {self.player_pos}")

        if message:
            self.display_message(message)

    def save_state(game,filename):
        # [title, geom, map, etc.]
        game_info = ["these", "nuts", game.map, game.player_pos, game.items, game.key]
        print(game_info)
        pickle.dump(game_info, open(filename, "wb"))

    def load_state(File):
        me = pickle.load(open(File, "rb"))
        return me


if __name__ == "__main__":
    game = Game()
    game.mainloop()