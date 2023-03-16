from random import randint


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску!"


class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"


class BoardWrongShipException(BoardException):
    pass


class Ship:
    def __init__(self, head, lives, direction):
        self.head = head
        self.l = lives
        self.direction = direction
        self.lives = lives
    @property
    def dots(self):
        ship_dots = []
        for i in range(self.lives):
            cur_x = self.head.x
            cur_y = self.head.y

            if self.direction == 0:
                cur_x += i

            elif self.direction == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    def shot_down(self, broadside):
        return broadside in self.dots


ship1 = Ship(Dot(1, 2), 2, 0)
print(ship1.shot_down(Dot(2, 4)))
