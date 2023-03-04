def greet():
    print('''Добро пожаловать в игру крестики-нолики
---------------------------------------
формат ввода координат: х y                      
х - номер по горизонтали    
y - номер по вертикали''')


def playing_field(field):
    print('''
    | 0 | 1 | 2 | 
  --------------- ''')
    for i, row in enumerate(field):
        print(f'''  {i} | {' | '.join(row)} | 
  --------------- 
              ''')


def ask_player(field):
    while True:
        player_move = input(f'         Ваш ход: ').split()
        if len(player_move) != 2:
            print('Введите две координаты через пробел: "x y"')
            continue
        x, y = player_move
        if x.isdigit() and y.isdigit():
            x, y = int(x), int(y)
            if 0 > x or x > 2 or 0 > y or y > 2:
                print(" Выход за предел игрового поля! ")
                continue
            elif field[x][y] != " ":
                print("Клетка занята!")
                continue
            else:
                return x, y
        else:
            print('Ведите координаты цифрами через пробел!')
            continue


def check(field):
    winning_combinations = (((0, 0), (0, 1), (0, 2)), ((1, 0), (1, 1), (1, 2)),
                            ((2, 0), (2, 1), (2, 2)),
                            ((0, 2), (1, 1), (2, 0)), ((0, 0), (1, 1), (2, 2)),
                            ((0, 0), (1, 0), (2, 0)),
                            ((0, 1), (1, 1), (2, 1)), ((0, 2), (1, 2), (2, 2)))
    for comb in winning_combinations:
        symbols = []
        for c in comb:
            symbols.append(field[c[0]][c[1]])
        if symbols == ["X", "X", "X"]:
            print("Выиграл X!!!")
            return True
        if symbols == ["O", "O", "O"]:
            print("Выиграл O!!!")
            return True
    return False


def game():
    greet()
    field = [[" "] * 3 for i in range(3)]
    step = 0
    while True:
        step += 1
        playing_field(field)
        if step % 2 == 1:
            print(" Ход крестика!")
        else:
            print(" Ходит нолик!")
        x, y = ask_player(field)
        if step % 2 == 1:
            field[x][y] = "X"
        else:
            field[x][y] = "O"

        if check(field):
            break
        if step == 9:
            print(" Ничья!\n Победила дружба")
            break


game()
