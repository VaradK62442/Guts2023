import _tkinter as tk

class Item:
    def __init__(self, name, description, representation, position, ascii_art="", action=None):
        self.name = name
        self.description = description
        self.representation = representation
        self.position = position
        self.ascii_art = ascii_art
        self.action = action  # Function to be called when the item is interacted with

    def __repr__(self):
        return self.representation