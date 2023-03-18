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
        return "Слишком далеко!!!\n Стрельба за пределы поля невозможна!!!"


class BoardUsedException(BoardException):
    def __str__(self):
        return "Уже стрелял!!!\n Перезаряжай и попробуй снова!!!"


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
                        "Отправлен ко дну!!!", 'Отправлен на корм рыбам!!!',
                        'Покойся с миром!!!']
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
        for i in ship.dots:
            if i in ship.dots:
                self.arena[i.x][i.y] = '⛵'
                self.busy.append(i)
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


class Player:
    def __init__(self, arena, enemy):
        self.arena = arena
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as exc:
                print(exc)


class Computer(Player):
    def ask(self):
        dot = Dot(randint(0, 9), randint(0, 9))
        print(f'Ход противника: {dot.x + 1} {User.words.setdefault(dot.y)}')
        return dot


class User(Player):
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy
        self.words = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'F': 4, 'G': 5, 'H': 6,
                      'I': 7,
                      'J': 8, 'K': 9}

    def ask(self):
        while True:
            dots = list(input('Ваш ход: ').replace(" ", "")).sort()
            if len(dots) != 2:
                print("Куда наводиться? Непонятно")
                print("Введите 2 координаты!!! ")
                continue
            if not(dots[1] in self.words):
                BoardOutException()
                continue
            if not (dots[0].isdigit()) or not (dots[1].isalpha()):
                print("Введите корректные координаты!!!")
                print("Ведите: цифру и букву")
                continue
            x, y = int(dots[0]), self.words.get(dots[1].upper())
            return Dot(x - 1, y)


class Game:
    def __init__(self, size=10):
        self.size = size
        desk1 = self.random_arena()
        desk2 = self.random_arena()
        desk2.hidden = True
        self.comp = Computer(desk2, desk1)
        self.us = User(desk1, desk2)

    def random_arena(self):
        desk = None
        while desk is None:
            desk = self.random_place()
        return desk

    def random_place(self):
        lens_ships = [3, 3, 2, 2, 2, 1, 1, 1, 1]
        desk = BattleField(size=self.size)
        number_of_attempts = 0
        for i in lens_ships:
            while True:
                number_of_attempts += 1
                if number_of_attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)),
                            i, randint(0, 1))
                try:
                    desk.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        desk.begin()
        return desk

    def greet(self):
        print('''  🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷
    Добро пожаловать в игру     
       💥МОРСКОЙ БОЙ💥 
  🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷
    Формат ввода координат:🗺👇
    🎉 X Y или Y X без разницы🎉 
                               
    ❗X - цифра от 1 до 10❗   
    ❗Y -  от A до K❗         
  🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷🔷
''')


board = Game()
board.greet()
print(board)
