import pygame

pygame.init()
width = 800
height = 800
fps = 60
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption('Checkers')
screen.fill((153, 255, 204))
pygame.display.flip()
pygame.font.init()
text = pygame.font.SysFont('Times New Roman', 30)
clock = pygame.time.Clock()
clock.tick(fps)

GameOver = False

moves = []

#формирование списков фигур и их локаций
black_pieces = ['man', 'man', 'man', 'man',
                'man', 'man', 'man', 'man',
                'man', 'man', 'man', 'man']

black_locations = [(1, 0), (3, 0), (5, 0), (7, 0),
                   (0, 1), (2, 1), (4, 1), (6, 1),
                   (1, 2), (3, 2), (5, 2), (7, 2)]

white_pieces = ['man', 'man', 'man', 'man',
                'man', 'man', 'man', 'man',
                'man', 'man', 'man', 'man']

white_locations = [(0, 5), (2, 5), (4, 5), (6, 5),
                   (1, 6), (3, 6), (5, 6), (7, 6),
                   (0, 7), (2, 7), (4, 7), (6, 7)]

#загрузка фотографий фигур
white_man = pygame.image.load('white.png')
white_king = pygame.image.load('white_king.png')
black_man = pygame.image.load('black.png')
black_king = pygame.image.load('black_king.png')

#рисование доски
def draw_board():
    for column in range(8):
        for row in range(column % 2, 8, 2):
            pygame.draw.rect(screen, (255, 255, 255), (column * 100, row * 100, 100, 100))
            pygame.display.flip()

#расположение изображений фигур в соответсвии с их типом и локацией
def draw_pieces():
    for i in range(len(white_pieces)):
        if white_pieces[i] == 'man':
            screen.blit(white_man, (white_locations[i][0] * 100, white_locations[i][1] * 100))
        else:
            screen.blit(white_king, (white_locations[i][0] * 100, white_locations[i][1] * 100))
    for i in range(len(black_pieces)):
        if black_pieces[i] == 'man':
            screen.blit(black_man, (black_locations[i][0] * 100, black_locations[i][1] * 100))
        else:
            screen.blit(black_king, (black_locations[i][0] * 100, black_locations[i][1] * 100))

#точечное обновление экрана для удаления зеленого цвета при выборе клетки, чтобы игра была более плавной
def screen_update(column, row):
    pygame.draw.rect(screen, (153, 255, 204), (column * 100, row * 100, 100, 100))
    pygame.display.flip()

#описание возможных ходов шашки
def draw_man(moves, pos, colour):
    moves.clear()
    if colour == 'white':
        #ordinary movement
        if ((pos[0] + 1, pos[1] - 1) not in white_locations and
                (pos[0] + 1, pos[1] - 1) not in black_locations and pos[0] < 7 and pos[1] > 0):
            moves.append((pos[0] + 1, pos[1] - 1))
        if ((pos[0] - 1, pos[1] - 1) not in white_locations and
                (pos[0] - 1, pos[1] - 1) not in black_locations and pos[0] > 0 and pos[1] > 0):
            moves.append((pos[0] - 1, pos[1] - 1))
        #capturing movement
        if ((pos[0] + 1, pos[1] + 1) in black_locations and (pos[0] + 2, pos[1] + 2) not in black_locations
                and (pos[0] + 2, pos[1] + 2) not in white_locations and pos[0] < 6 and pos[1] < 6):
            moves.append((pos[0] + 2, pos[1] + 2))
        if ((pos[0] - 1, pos[1] + 1) in black_locations and (pos[0] - 2, pos[1] + 2) not in black_locations
                and (pos[0] - 2, pos[1] + 2) not in white_locations and pos[0] > 1 and pos[1] < 6):
            moves.append((pos[0] - 2, pos[1] + 2))
        if ((pos[0] + 1, pos[1] - 1) in black_locations and (pos[0] + 2, pos[1] - 2) not in black_locations
                and (pos[0] + 2, pos[1] - 2) not in white_locations and pos[0] < 6 and pos[1] > 1):
            moves.append((pos[0] + 2, pos[1] - 2))
        if ((pos[0] - 1, pos[1] - 1) in black_locations and (pos[0] - 2, pos[1] - 2) not in black_locations
                and (pos[0] - 2, pos[1] - 2) not in white_locations and pos[0] > 1 and pos[1] > 1):
            moves.append((pos[0] - 2, pos[1] - 2))
    else:
        #ordinary movement
        if ((pos[0] + 1, pos[1] + 1) not in black_locations and
                (pos[0] + 1, pos[1] + 1) not in white_locations and pos[0] < 7 and pos[1] < 7):
            moves.append((pos[0] + 1, pos[1] + 1))
        if ((pos[0] - 1, pos[1] + 1) not in black_locations and
                (pos[0] - 1, pos[1] + 1) not in white_locations and pos[0] > 0 and pos[1] < 7):
            moves.append((pos[0] - 1, pos[1] + 1))
        #capturing movement
        if ((pos[0] + 1, pos[1] + 1) in white_locations and (pos[0] + 2, pos[1] + 2) not in black_locations
                and (pos[0] + 2, pos[1] + 2) not in white_locations and pos[0] < 6 and pos[1] < 6):
            moves.append((pos[0] + 2, pos[1] + 2))
        if ((pos[0] - 1, pos[1] + 1) in white_locations and (pos[0] - 2, pos[1] + 2) not in black_locations
                and (pos[0] - 2, pos[1] + 2) not in white_locations and pos[0] > 1 and pos[1] < 6):
            moves.append((pos[0] - 2, pos[1] + 2))
        if ((pos[0] + 1, pos[1] - 1) in white_locations and (pos[0] + 2, pos[1] - 2) not in black_locations
                and (pos[0] + 2, pos[1] - 2) not in white_locations and pos[0] < 6 and pos[1] > 1):
            moves.append((pos[0] + 2, pos[1] - 2))
        if ((pos[0] - 1, pos[1] - 1) in white_locations and (pos[0] - 2, pos[1] - 2) not in black_locations
                and (pos[0] - 2, pos[1] - 2) not in white_locations and pos[0] > 1 and pos[1] > 1):
            moves.append((pos[0] - 2, pos[1] - 2))
    return moves

#описание возможных ходов дамки (требует дальнейшей доработки, так как не учитывает, есть ли фигуры на пути движения)
def draw_king(moves, pos, colour):
    moves.clear()
    if colour == 'white':
        for x in range(1, 8):
            if ((pos[0] + x, pos[1] + x) not in white_locations and
                    (pos[0] + x, pos[1] + x) not in black_locations):
                moves.append((pos[0] + x, pos[1] + x))
            if ((pos[0] + x, pos[1] - x) not in white_locations and
                    (pos[0] + x, pos[1] - x) not in black_locations):
                moves.append((pos[0] + x, pos[1] - x))
            if ((pos[0] - x, pos[1] + x) not in white_locations and
                    (pos[0] - x, pos[1] + x) not in black_locations):
                moves.append((pos[0] - x, pos[1] + x))
            if ((pos[0] - x, pos[1] - x) not in white_locations and
                    (pos[0] - x, pos[1] - x) not in black_locations):
                moves.append((pos[0] - x, pos[1] - x))
    else:
        for x in range(1, 8):
            if ((pos[0] + x, pos[1] + x) not in white_locations and
                    (pos[0] + x, pos[1] + x) not in black_locations):
                moves.append((pos[0] + x, pos[1] + x))
            if ((pos[0] + x, pos[1] - x) not in white_locations and
                    (pos[0] + x, pos[1] - x) not in black_locations):
                moves.append((pos[0] + x, pos[1] - x))
            if ((pos[0] - x, pos[1] + x) not in white_locations and
                    (pos[0] - x, pos[1] + x) not in black_locations):
                moves.append((pos[0] - x, pos[1] + x))
            if ((pos[0] - x, pos[1] - x) not in white_locations and
                    (pos[0] - x, pos[1] - x) not in black_locations):
                moves.append((pos[0] - x, pos[1] - x))
    return moves

#функция захвата фигур
def capture(pos, pos_new, pieces, locations):
    for x in range(1, 8):
        if pos[0] + x == pos_new[0] and pos[1] + x == pos_new[1]:
            for i in range(len(pieces)):
                if pos[0] < locations[i][0] < pos_new[0] and pos[1] < locations[i][1] < pos_new[1]:
                    locations.pop(i)
                    pieces.pop(i)
                    break
        if pos[0] + x == pos_new[0] and pos[1] - x == pos_new[1]:
            for i in range(len(pieces)):
                if pos[0] < locations[i][0] < pos_new[0] and pos[1] > locations[i][1] > pos_new[1]:
                    locations.pop(i)
                    pieces.pop(i)
                    break
        if pos[0] - x == pos_new[0] and pos[1] + x == pos_new[1]:
            for i in range(len(pieces)):
                if pos[0] > locations[i][0] > pos_new[0] and pos[1] < locations[i][1] < pos_new[1]:
                    locations.pop(i)
                    pieces.pop(i)
                    break
        if pos[0] - x == pos_new[0] and pos[1] - x == pos_new[1]:
            for i in range(len(pieces)):
                if pos[0] > locations[i][0] > pos_new[0] and pos[1] > locations[i][1] > pos_new[1]:
                    locations.pop(i)
                    pieces.pop(i)
                    break

#превращение шашки в дамку, меняет тип фигуры в списке
def coronation():
    for i in range(len(black_locations)):
        if black_locations[i][1] == 7:
            black_pieces[i] = 'king'
    for i in range(len(white_locations)):
        if white_locations[i][1] == 0:
            white_pieces[i] = 'king'

#описание возможных ходов фигур
def draw(pieces, moves, locations, pos, colour):
    i = locations.index(pos)
    if pieces[i] == 'man':
        draw_man(moves, pos, colour)
    else:
        draw_king(moves, pos, colour)
    return moves

#меняет локацию фигуры в списке
def change_location(moves, locations, pos, pos_new):
    if pos_new in moves:
        for i in range(len(locations)):
            if locations[i] == pos:
                locations[i] = pos_new
    return locations

#проверяет количество фигур и возращает номер победителя, если у одного из игроков не осталось фигур
def check_figures(pieces):
    if len(pieces) == 0:
        return 1
    else:
        return 0

#конец игры, вызывается в случае, если у игрока не осталось фигур в списке (до сих пор не вызывалась)
def game_over():
    screen.fill((0, 0, 0))
    pygame.display.flip()
    text_surface = text.render('Game over!', True, (255, 0, 0))
    screen.blit(text_surface, (0, 0))

#игра, вызов функций
pos = (-1, -1)
q = True
while q:
    check_figures(white_pieces)
    check_figures(black_pieces)

    if check_figures(white_pieces) or check_figures(black_pieces):
        GameOver = True
        game_over()

    if GameOver == False:
        draw_board()
        draw_pieces()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            q = False
        if event.type == pygame.MOUSEBUTTONUP and GameOver == False:
            column = event.pos[0] // 100
            row = event.pos[1] // 100
            pos = (column, row)
            print("pos", pos)
            pygame.draw.rect(screen, (0, 255, 0), (column * 100, row * 100, 100, 100)) #обозначение выбранной клетки
            pygame.display.flip()

        if event.type == pygame.MOUSEBUTTONDOWN and pos in white_locations and GameOver == False:
            draw(white_pieces, moves, white_locations, pos, 'white')
            print("moves", moves)
            column_new = event.pos[0] // 100
            row_new = event.pos[1] // 100
            pos_new = (column_new, row_new)
            print("pos_new", pos_new)
            change_location(moves, white_locations, pos, pos_new)
            print("white_locations", white_locations)
            if pos_new in moves:
                capture(pos, pos_new, black_pieces, black_locations)
            coronation()
            for x in range(0, 8):
                screen_update(column + x, row + x)
                screen_update(column + x, row - x)
                screen_update(column - x, row + x)
                screen_update(column - x, row - x)
            draw_board()
            draw_pieces()

        if event.type == pygame.MOUSEBUTTONDOWN and pos in black_locations and GameOver == False:
            draw(black_pieces, moves, black_locations, pos, 'black')
            print("moves", moves)
            column_new = event.pos[0] // 100
            row_new = event.pos[1] // 100
            pos_new = (column_new, row_new)
            print("pos_new", pos_new)
            change_location(moves, black_locations, pos, pos_new)
            print("black_locations", black_locations)
            if pos_new in moves:
                capture(pos, pos_new, white_pieces, white_locations)
            coronation()
            for x in range(0, 8):
                screen_update(column + x, row + x)
                screen_update(column + x, row - x)
                screen_update(column - x, row + x)
                screen_update(column - x, row - x)
            draw_board()
            draw_pieces()

        if event.type == pygame.KEYDOWN and GameOver: #повторная игра
            GameOver = False

            moves = []

            black_pieces = ['man', 'man', 'man', 'man',
                            'man', 'man', 'man', 'man',
                            'man', 'man', 'man', 'man']

            black_locations = [(1, 0), (3, 0), (5, 0), (7, 0),
                               (0, 1), (2, 1), (4, 1), (6, 1),
                               (1, 2), (3, 2), (5, 2), (7, 2)]

            white_pieces = ['man', 'man', 'man', 'man',
                            'man', 'man', 'man', 'man',
                            'man', 'man', 'man', 'man']

            white_locations = [(0, 5), (2, 5), (4, 5), (6, 5),
                               (1, 6), (3, 6), (5, 6), (7, 6),
                               (0, 7), (2, 7), (4, 7), (6, 7)]

            screen.fill((153, 255, 204))
            pygame.display.flip()


pygame.quit()
