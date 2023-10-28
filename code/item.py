class Item:
    def __init__(self, name, description, representation, position, ascii_art=""):
        self.name = name
        self.description = description
        self.representation = representation
        self.position = position
        self.ascii_art = ascii_art

    def __repr__(self):
        return self.representation