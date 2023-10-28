from item import Item

class Map:

    def __init__(self, dimensions):
        self.dimen = dimensions  # [x, y]
        self.user_map()

    def user_map(self):
        self.arr = []
        for y in range(self.dimen[1]):
            self.arr.append([None] * self.dimen[0])
            for x in range(self.dimen[0]):
                if x == 0 or x == self.dimen[0] - 1:
                    self.arr[y][x] = "|"
                elif y == 0 or y == self.dimen[1] - 1:
                    self.arr[y][x] = "-"
                else:
                    self.arr[y][x] = "."

        self.add_to_map("D", [0, 5])  # Add a door at position (0, 5)

    def show_map(self, canvas):
        canvas.delete("all")
        for y in range(self.dimen[1]):
            for x in range(self.dimen[0]):
                canvas.create_text(x * 20 + 10, y * 20 + 10, text=self.arr[y][x], fill="white", font=('Arial', 20))

    def add_to_map(self, object, position):
        if isinstance(object, Item):
            self.arr[position[1]][position[0]] = object.representation
        elif object == "⯌":
            self.arr[position[1]][position[0]] = "⯌"  # "⯌" represents the player
        elif object == "D":
            self.arr[position[1]][position[0]] = "D"  # "D" represents the door
        elif object == "S":
            self.arr[position[1]][position[0]] = "S"
        else:
            self.arr[position[1]][position[0]] = object

    def reset(self, items, inventory, player_pos):
        self.user_map()
        for item in inventory:
            self.add_to_map(item, item.position)
        self.add_to_map("⯌", player_pos)