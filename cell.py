from graphics import Line, Point


class Cell:
    def __init__(self, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self._win = win

    def draw(self, x1, y1, x2, y2):
        def get_wall_color(has_wall):
            return "black" if has_wall else "white"

        def has_wall(cell):
            return lambda dir: getattr(cell, f"has_{dir}_wall")

        def get_dirs(x1, y1, x2, y2):
            return {
                "left": ((x1, y1), (x1, y2)),
                "right": ((x2, y1), (x2, y2)),
                "top": ((x1, y1), (x2, y1)),
                "bottom": ((x1, y2), (x2, y2)),
            }

        def assign_attrs():
            self._x1 = x1
            self._x2 = x2
            self._y1 = y1
            self._y2 = y2

        if self._win is None:
            return

        assign_attrs()

        has_wall_in_dir = has_wall(self)

        for direction in ["left", "right", "top", "bottom"]:
            (start, end) = get_dirs(x1, y1, x2, y2)[direction]
            wall_color = get_wall_color(has_wall_in_dir(direction))
            line = Line(Point(*start), Point(*end))

            self._win.draw_line(line, wall_color)

    def draw_move(self, to_cell, undo=False):
        if self._win is None:
            return

        fill_color = "gray" if undo else "red"

        def to_mid(cell):
            return (cell._x1 + cell._x2) / 2, (cell._y1 + cell._y2) / 2

        def draw_line_in_dir(direction):
            x_mid, y_mid = to_mid(self)
            to_x_mid, to_y_mid = to_mid(to_cell)

            directions = {
                "left": [
                    ((self._x1, y_mid), (x_mid, y_mid)),
                    ((to_x_mid, to_y_mid), (to_cell._x2, to_y_mid)),
                ],
                "right": [
                    ((x_mid, y_mid), (self._x2, y_mid)),
                    ((to_cell._x1, to_y_mid), (to_x_mid, to_y_mid)),
                ],
                "top": [
                    ((x_mid, self._y1), (x_mid, y_mid)),
                    ((to_x_mid, to_cell._y2), (to_x_mid, to_y_mid)),
                ],
                "bottom": [
                    ((x_mid, y_mid), (x_mid, self._y2)),
                    ((to_x_mid, to_y_mid), (to_x_mid, to_cell._y1)),
                ],
            }
            for lines in directions[direction]:
                line = Line(Point(*lines[0]), Point(*lines[1]))
                self._win.draw_line(line, fill_color)

        if self._x1 > to_cell._x1:
            draw_line_in_dir("left")
        elif self._x1 < to_cell._x1:
            draw_line_in_dir("right")
        elif self._y1 > to_cell._y1:
            draw_line_in_dir("top")
        elif self._y1 < to_cell._y1:
            draw_line_in_dir("bottom")
