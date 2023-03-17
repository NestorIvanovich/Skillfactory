from random import randint, choice


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
        self.phrases = ['Готов!!!', "Корабль уничтожен!!!", 'Лихо ты его!!!',
                        "Нагнул теперь он увидит где крабы зимуют!!",
                        "Отправлен ко дну!!!", 'Отправлен на корм рыбам!!!']
        self.wounded = ['Есть попадание!!', "Цель захвачена!!!",
                        "одной ногой в могиле!!!",
                        "Противник горит продолжай в том же духе!!!",
                        "Точный выстрел!!!"]
        self.miss = ['Мимо!', "что за возня!?", "Промахнулся!!!",
                     "Эх, не попал!!!", "Хватит впустую снаряды тратить!!!"]

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

    def add_ship(self, ship):
        for i in ship.dots:
            if self.outside(i) or i in self.busy:
                raise BoardWrongShipException()
            if i in ship.dots:
                self.arena[ship.x][ship.y] = '⛵'
                self.busy.append(ship)
        self.ships.append(ship)
        self.ship_contour(ship)

    def ship_contour(self, ship, verb=False):
        ship_boundary = [(-1, -1), (-1, 0), (-1, 1),
                         (0, -1), (0, 0), (0, 1),
                         (1, -1), (1, 0), (1, 1)]
        for i in ship.dots:
            for ix, iy in ship_boundary:
                current = Dot(i.x + ix, i.y + iy)
                if not (self.outside(current)) and current not in self.busy:
                    if verb:
                        self.arena[current.x][current.y] = '⬛'
                        self.busy.append(current)

    def gun(self, dot):
        if self.outside(dot):
            raise BoardOutException()
        if dot in self.busy:
            raise BoardUsedException()
        self.busy.append(dot)
        for ship in self.ships:
            if dot in ship.dots:
                ship.lives -= 1
                self.arena[dot.x][dot.y] = '❌'
                if ship.lives == 0:
                    self.affected += 1
                    self.ship_contour(ship, verb=True)
                    print(choice(self.phrases))
                    return False
                else:
                    print(choice(self.wounded))
                    return True
        self.arena[dot.x][dot.y] = '🎯'
        print(choice(self.miss))
        return False

    def begin(self):
        self.busy = []


board = BattleField()
board.ship_contour(Ship(Dot(3, 3), 5, 1), True)
#print(board)

print(a)