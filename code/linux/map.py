from item import Item


class Map:

    def __init__(self, dimensions, door_locations):
        self.dimen = dimensions  # [x, y]
        self.user_map(door_locations)
        self.player_pos = None

    def user_map(self, door_locations):

        # print("doors: ", door_locations)

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

        # add doors
        for door in door_locations:
            self.add_to_map(
                "D", door) if door_locations[door][1] else self.add_to_map(".", door)

    def show_map2(self, canvas):
        print("show map called")
        canvas.delete("all")
        canvas.update()  # Force the canvas to update its size
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        map_width = self.dimen[0] * 20
        map_height = self.dimen[1] * 20
        offset_x = (canvas_width - map_width) // 2
        offset_y = (canvas_height - map_height) // 2
        for y in range(self.dimen[1]):
            for x in range(self.dimen[0]):
                canvas.create_text(
                    offset_x + x * 20 + 10, offset_y + y * 20 + 10, text=self.arr[y][x], fill="white", font=('Arial', 20))
                
    def show_map(self, canvas):
        canvas.delete("all")
        for y in range(self.dimen[1]):
            for x in range(self.dimen[0]):
                canvas.create_text(x * 20 + 10, y * 20 + 10, text=self.arr[y][x], fill="white", font=('Arial', 20))


    def add_to_map(self, object, position):
        if isinstance(object, Item):
            self.arr[position[1]][position[0]] = object.representation
        elif object == "⯌":
            # "⯌" represents the player
            self.arr[position[1]][position[0]] = "⯌"
        elif object == "D":
            self.arr[position[1]][position[0]] = "D"  # "D" represents the door
        elif object == "S":
            self.arr[position[1]][position[0]] = "S"
        else:
            try:
                self.arr[position[1]][position[0]] = object
            except Exception as e:
                pass

    def reset(self, items, inventory, player_pos):
        self.user_map()
        for item in inventory:
            self.add_to_map(item, item.position)
        self.add_to_map("⯌", player_pos)
