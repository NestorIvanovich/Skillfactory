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


class BattleField:
    def __init__(self, hidden=False, size=10):
        self.hidden = hidden
        self.size = size
        self.affected = 0
        self.arena = [['🌊'] * size for i in range(size)]
        self.busy = []
        self.ships = []

    def __str__(self):
        field = ''
        field += '     A    B    C     D    F    G    H    I    J    K  '
        for i, row in enumerate(self.arena):
            if i < 9:
                field += f'\n {i + 1} | ' + ' | '.join(row) + ' |'
            else:
                field += f'\n{i + 1} | ' + ' | '.join(row) + ' |'
        if self.hidden:
            field = field.replace('⛵', '🌊')
        return field

    def outside(self, dot):
        return not ((0 <= dot.x < self.size) and (0 <= dot.y < self.size))


board = BattleField()
print(board)
