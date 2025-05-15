from pygame import mixer
import pygame
import copy

pygame.init()
width = 800
height = 1000
fps = 60
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption('Checkers')
screen.fill((153, 255, 204))
pygame.draw.rect(screen, (0, 0, 0), (0, 800, 800, 1000))
pygame.display.flip()
pygame.font.init()
text = pygame.font.SysFont('Times New Roman', 30)
text_count_white = pygame.font.SysFont('Times New Roman', 30)
text_count_black = pygame.font.SysFont('Times New Roman', 30)
mixer.init()
mixer.music.load('victory_sound.wav')
clock = pygame.time.Clock()
clock.tick(fps)

GameOver = False #флаг для конца игры
turn = 'white' #текущий ход
prev_turn = 'white' #предыдущий ход
next_turn = 'white' #следующий ход
count_white = 0 #счетчик побед белых фигур
count_black = 0 #счетчик побед черных фигур
curr_piece_1 = [-1, -1] #начальная локация выбранной фигуры
curr_piece_2 = [-1, -1] #конечная локация выбранной фигуры
curr_piece_type = 0 #тип выбранной фигуры

moves = [] #массив возможных ходов

#формирование списков фигур и их локаций (замена "man" и "king" на 1 и 2 соотвественно)
black_pieces = [1] * 12

black_locations = [(1, 0), (3, 0), (5, 0), (7, 0),
                   (0, 1), (2, 1), (4, 1), (6, 1),
                   (1, 2), (3, 2), (5, 2), (7, 2)]

white_pieces = [1] * 12

white_locations = [(0, 5), (2, 5), (4, 5), (6, 5),
                   (1, 6), (3, 6), (5, 6), (7, 6),
                   (0, 7), (2, 7), (4, 7), (6, 7)]

#фигуры и позиции при предыдущем ходе
prev_black_pieces = black_pieces
prev_black_locations = black_locations
prev_white_pieces = white_pieces
prev_white_locations = white_locations

#фигуры и позиции при следующем ходе
next_black_pieces = black_pieces
next_black_locations = black_locations
next_white_pieces = white_pieces
next_white_locations = white_locations

free_pieces = [] #фигуры, которыми можно ходить (выделяются желтым)
free_locations = [] #их локации

#загрузка фотографий фигур
white_man = pygame.image.load('white.png')
white_king = pygame.image.load('white_king.png')
black_man = pygame.image.load('black.png')
black_king = pygame.image.load('black_king.png')
undo_button = pygame.image.load('undo_button.png')
flag = pygame.image.load('flag.png')
redo_button = pygame.image.load('redo_button.png')

#рисование доски
def draw_board():
    for column in range(8):
        for row in range(column % 2, 8, 2):
            pygame.draw.rect(screen, (255, 255, 255), (column * 100, row * 100, 100, 100))
            pygame.display.flip()

#расположение изображений фигур в соответсвии с их типом и локацией
def draw_pieces():
    for i in range(len(white_pieces)):
        if white_pieces[i] == 1:
            screen.blit(white_man, (white_locations[i][0] * 100, white_locations[i][1] * 100))
        else:
            screen.blit(white_king, (white_locations[i][0] * 100, white_locations[i][1] * 100))
    for i in range(len(black_pieces)):
        if black_pieces[i] == 1:
            screen.blit(black_man, (black_locations[i][0] * 100, black_locations[i][1] * 100))
        else:
            screen.blit(black_king, (black_locations[i][0] * 100, black_locations[i][1] * 100))

#расположение изображений кнопок
def buttons():
    screen.blit(undo_button, (270, 900))
    screen.blit(flag, (370, 900))
    screen.blit(redo_button, (470, 900))

#точечное обновление экрана (обновление полей при перемещении фигур)
def screen_update_1(pos):
    pygame.draw.rect(screen, (153, 255, 204), (pos[0] * 100, pos[1] * 100, 100, 100))
    pygame.display.flip()

#точечное обновление экрана (выделение полей)
def screen_update_2():
    for column in range(1, 8, 2):
        pygame.draw.rect(screen, (153, 255, 204), (column * 100, 0, 100, 100), 5)
    for column in range(8):
        for row in range(column % 2 + 1, 8, 2):
            pygame.draw.rect(screen, (153, 255, 204), (column * 100, row * 100, 100, 100), 5)
    pygame.display.flip()

#сохранение предыдущего хода
def copy_1(turn):
    global prev_turn, prev_black_pieces, prev_black_locations, prev_white_pieces, prev_white_locations
    prev_turn = turn
    prev_black_pieces = copy.deepcopy(black_pieces)
    prev_black_locations = copy.deepcopy(black_locations)
    prev_white_pieces = copy.deepcopy(white_pieces)
    prev_white_locations = copy.deepcopy(white_locations)

#сохранение текущего хода
def copy_2(turn):
    global next_turn, next_black_pieces, next_black_locations, next_white_pieces, next_white_locations
    next_turn = turn
    next_black_pieces = copy.deepcopy(black_pieces)
    next_black_locations = copy.deepcopy(black_locations)
    next_white_pieces = copy.deepcopy(white_pieces)
    next_white_locations = copy.deepcopy(white_locations)

#описание возможных ходов шашки (если есть ходы захвата нельзя ходить обычными ходами)
def draw_man(moves, pos, colour):
    moves.clear()
    if colour == 'white':
        directions = [(1, -1), (-1, -1)]
        enemy_locations = black_locations
        own_locations = white_locations
    else:
        directions = [(1, 1), (-1, 1)]
        enemy_locations = white_locations
        own_locations = black_locations
    capture_directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    for dx, dy in capture_directions: #если найдутся движения захвата, фигура не сможет сходить обычным ходом
        new_x, new_y = pos[0] + dx, pos[1] + dy
        jump_x, jump_y = pos[0] + 2 * dx, pos[1] + 2 * dy
        if (0 <= new_x < 8 and 0 <= new_y < 8 and (new_x, new_y) in enemy_locations and
                0 <= jump_x < 8 and 0 <= jump_y < 8 and (jump_x, jump_y) not in own_locations and
                (jump_x, jump_y) not in enemy_locations):
            moves.append((jump_x, jump_y))
    if moves:
        return moves
    for dx, dy in directions: #обычный ход (если нет движений захвата)
        new_x, new_y = pos[0] + dx, pos[1] + dy
        if 0 <= new_x < 8 and 0 <= new_y < 8:
            if (new_x, new_y) not in own_locations and (new_x, new_y) not in enemy_locations:
                moves.append((new_x, new_y))
    return moves

#описание возможных ходов дамки
def draw_king(moves, pos, colour):
    moves.clear()
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    if colour == 'white':
        enemy_locations = black_locations
        own_locations = white_locations
    else:
        enemy_locations = white_locations
        own_locations = black_locations

    for dx, dy in directions:
        f = 0
        for step in range(1, 8):
            new_x, new_y = pos[0] + dx * step, pos[1] + dy * step
            if 0 <= new_x <= 7 and 0 <= new_y <= 7:
                new_pos = (new_x, new_y)
                if new_pos in own_locations: #клетка занята фигурой своего цвета
                    break
                elif new_pos in enemy_locations: #клетка занята фигурой вражеского цвета
                    if f:
                        break
                    f = 1
                else: #клетка свободна
                    if f: #т.к. цикл шага от 1 до 8, до этого встретилась фигура вражеского цвета (она будет между начальной и конечной позициями активной фигуры)
                        moves.append(new_pos)
                        break
                    else:
                        moves.append(new_pos)
            else: #выход за пределы поля
                break
    return moves

#описание возможных ходов фигур
def draw(moves, pieces, locations, pos, colour):
    i = locations.index(pos)
    draw_man(moves, pos, colour) if pieces[i] == 1 else draw_king(moves, pos, colour)
    return moves

#функция удаления захваченной фигуры
def capture(pos, pos_new, pieces, locations):
    dx, dy = (pos_new[0] - pos[0]), (pos_new[1] - pos[1])
    step_x = dx // abs(pos_new[0] - pos[0]) if pos_new[0] != pos[0] else 0
    step_y = dy // abs(pos_new[1] - pos[1]) if pos_new[1] != pos[1] else 0

    pos_x, pos_y = pos
    while (pos_x, pos_y) != pos_new: #проходится между начальной и конечной позициями фигуры и проверяет, нет ли этих локаций в массиве локаций
        pos_x += step_x
        pos_y += step_y
        captured_pos = (pos_x, pos_y)
        if captured_pos in locations:
            index = locations.index(captured_pos)
            locations.pop(index)
            pieces.pop(index)
            screen_update_1(captured_pos)

#функция проверки возможности дополнительных ходов
def check_additional_captures(pos, colour, pieces, locations):
    moves.clear()
    i = locations.index(pos)
    draw_man(moves, pos, colour) if pieces[i] == 1 else draw_king(moves, pos, colour)
    return any(abs(new_pos_x - pos[0]) > 1 for (new_pos_x, new_pos_y) in moves)

#функция формирования нового массива с фигурами, которые можно двигать и выделения их желтым цветом
def check_free_pieces(colour):
    free_pieces.clear()
    if colour == 'white':
        enemy_locations = black_locations
        own_locations = white_locations
        own_pieces = white_pieces
    else:
        enemy_locations = white_locations
        own_locations = black_locations
        own_pieces = black_pieces
    capture_directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    f2 = 0

    for i in range(len(own_pieces)):
        f1 = 0
        for dx, dy in capture_directions:
            new_x, new_y = own_locations[i][0] + dx, own_locations[i][1] + dy
            jump_x, jump_y = own_locations[i][0] + 2 * dx, own_locations[i][1] + 2 * dy
            if (0 <= nx < 8 and 0 <= ny < 8 and
                    (nx, ny) in enemy_locations and
                    0 <= jump_x < 8 and 0 <= jump_y < 8 and
                    (jump_x, jump_y) not in own_locations and
                    (jump_x, jump_y) not in enemy_locations):
                f1 = 1
        if f1:
            f2 = 1
            free_pieces.append(own_pieces[i])
            pygame.draw.rect(screen, (255, 255, 0), (own_locations[i][0] * 100, own_locations[i][1] * 100, 100, 100), 5)
            pygame.display.flip()
    if f2:
        return free_pieces
    else:
        free_pieces.extend(own_pieces)
        for i in range(len(free_pieces)):
            pygame.draw.rect(screen, (255, 255, 0), (own_locations[i][0] * 100, own_locations[i][1] * 100, 100, 100), 5)
        return free_pieces

#функция формирования нового массива с локациями
def check_free_locations(colour):
    free_locations.clear()
    if colour == 'white':
        enemy_locations = black_locations
        own_locations = white_locations
        own_pieces = white_pieces
    else:
        enemy_locations = white_locations
        own_locations = black_locations
        own_pieces = black_pieces
    capture_directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    f2 = 0

    for i in range(len(own_pieces)):
        f1 = 0
        for dx, dy in capture_directions:
            new_x, new_y = own_locations[i][0] + dx, own_locations[i][1] + dy
            jump_x, jump_y = own_locations[i][0] + 2 * dx, own_locations[i][1] + 2 * dy
            if (0 <= new_x < 8 and 0 <= new_y < 8 and
                    (new_x, new_y) in enemy_locations and
                    0 <= jump_x < 8 and 0 <= jump_y < 8 and
                    (jump_x, jump_y) not in own_locations and
                    (jump_x, jump_y) not in enemy_locations):
                f1 = 1
        if f1:
            f2 = 1
            free_locations.append(own_locations[i])
    if f2:
        return free_locations
    else:
        free_locations.extend(own_locations)
        return free_locations

#превращение шашки в дамку, меняет тип фигуры с 1 на 2 в списке
def coronation():
    for i in range(len(black_locations)):
        if black_locations[i][1] == 7:
            black_pieces[i] = 2
    for i in range(len(white_locations)):
        if white_locations[i][1] == 0:
            white_pieces[i] = 2

#изменение локации фигуры в списке
def change_location(moves, locations, pos, pos_new):
    if pos_new in moves:
        for i in range(len(locations)):
            if locations[i] == pos:
                locations[i] = pos_new
    return locations

#проверка количества фигур и возращает цвет победителя, если у одного из игроков не осталось фигур
def check_figures():
    if len(white_pieces) == 0:
        return 'black'
    if len(black_pieces) == 0:
        return 'white'
    else:
        return 1

#обновление счета побед
def victory_count():
    text_count_white = f"white: {count_white}"
    upd_text_count_white = text.render(text_count_white, True, (255, 255, 255))
    screen.blit(upd_text_count_white, (0, 820))
    text_count_black = f"black: {count_black}"
    upd_text_count_black = text.render(text_count_black, True, (255, 255, 255))
    screen.blit(upd_text_count_black, (0, 860))

#конец игры
def game_over(colour):
    screen.fill((0, 0, 0))
    upd_text = text.render((f"game over! {colour} has won"), True, (255, 0, 0))
    screen.blit(upd_text, (250, 450))
    mixer.music.play()
    pygame.display.flip()

#обновление информации после конца игры
def reset():
    global black_pieces, black_locations, white_pieces, white_locations
    global prev_black_pieces, prev_black_locations, prev_white_pieces, prev_white_locations
    global next_black_pieces, next_black_locations, next_white_pieces, next_white_locations
    global free_pieces, free_locations
    global GameOver, turn, prev_turn, next_turn
    global curr_piece_1, curr_piece_2, curr_piece_type
    global moves, pos, f

    black_pieces = [1] * 12

    black_locations = [(1, 0), (3, 0), (5, 0), (7, 0),
                       (0, 1), (2, 1), (4, 1), (6, 1),
                       (1, 2), (3, 2), (5, 2), (7, 2)]

    white_pieces = [1] * 12

    white_locations = [(0, 5), (2, 5), (4, 5), (6, 5),
                       (1, 6), (3, 6), (5, 6), (7, 6),
                       (0, 7), (2, 7), (4, 7), (6, 7)]

    prev_black_pieces = []
    prev_black_locations = []
    prev_white_pieces = []
    prev_white_locations = []

    next_black_pieces = []
    next_black_locations = []
    next_white_pieces = []
    next_white_locations = []

    free_pieces = []
    free_locations = []

    GameOver = False
    turn = 'white'
    prev_turn = 'white'
    next_turn = 'white'
    curr_piece_1 = [-1, -1]
    curr_piece_2 = [-1, -1]
    curr_piece_type = 0

    moves = []

    pos = (-1, -1)
    f = 1
    screen.fill((153, 255, 204))
    pygame.draw.rect(screen, (0, 0, 0), (0, 800, 800, 1000))
    draw_board()
    draw_pieces()
    victory_count()
    buttons()
    pygame.display.flip()

#игра, вызов функций
victory_count()
buttons()
pygame.display.flip()
pos = (-1, -1)
f = 1
q = True
while q:
    winner = check_figures()

    if winner != 1:
        if winner == 'black':
            count_black += 1
        else:
            count_white += 1
        GameOver = True
        game_over(winner)

    if not GameOver:
        draw_board()
        draw_pieces()

    if f and not GameOver:
        check_free_pieces('white')
        check_free_locations('white')
        f = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            q = False

        if event.type == pygame.MOUSEBUTTONUP and not GameOver:
            column = event.pos[0] // 100
            row = event.pos[1] // 100
            pos = (column, row)
            if row < 8:
                pygame.draw.rect(screen, (0, 255, 0), (column * 100, row * 100, 100, 100), 5)
            pygame.display.flip()

        #обработка хода белых
        if event.type == pygame.MOUSEBUTTONDOWN and turn == 'white' and pos in free_locations and not GameOver:
            draw(moves, free_pieces, free_locations, pos, 'white')
            column_new = event.pos[0] // 100
            row_new = event.pos[1] // 100
            pos_new = (column_new, row_new)
            curr_piece_1 = pos
            curr_piece_2 = pos_new
            curr_piece_type = free_pieces[free_locations.index(pos)]
            copy_1(turn)
            if pos_new in moves:
                change_location(moves, white_locations, pos, pos_new)
                coronation()
                screen_update_1(pos)
                screen_update_2()
                draw_pieces()
                copy_2('black')
                if abs(pos_new[0] - pos[0]) > 1:
                    capture(pos, pos_new, black_pieces, black_locations)
                    screen_update_1(pos)
                    screen_update_2()
                    draw_pieces()
                    if check_additional_captures(pos_new, 'white', white_pieces, white_locations):
                        pos = pos_new
                        check_free_pieces('white')
                        check_free_locations('white')
                        continue #продолжение хода той же шашкой
                    else:
                        turn = 'black'
                        check_free_pieces('black')
                        check_free_locations('black')
                else:
                    turn = 'black'
                    check_free_pieces('black')
                    check_free_locations('black')

        #обработка хода черных
        if event.type == pygame.MOUSEBUTTONDOWN and turn == 'black' and pos in free_locations and not GameOver:
            draw(moves, free_pieces, free_locations, pos, 'black')
            column_new = event.pos[0] // 100
            row_new = event.pos[1] // 100
            pos_new = (column_new, row_new)
            curr_piece_1 = pos
            curr_piece_2 = pos_new
            curr_piece_type = free_pieces[free_locations.index(pos)]
            copy_1(turn)
            if pos_new in moves:
                change_location(moves, black_locations, pos, pos_new)
                coronation()
                screen_update_1(pos)
                screen_update_2()
                draw_pieces()
                copy_2('white')
                if abs(pos_new[0] - pos[0]) > 1:
                    capture(pos, pos_new, white_pieces, white_locations)
                    screen_update_1(pos)
                    screen_update_2()
                    draw_pieces()
                    if check_additional_captures(pos_new, 'black', black_pieces, black_locations):
                        pos = pos_new
                        check_free_pieces('black')
                        check_free_locations('black')
                        continue #продолжение хода той же шашкой
                    else:
                        turn = 'white'
                        check_free_pieces('white')
                        check_free_locations('white')
                else:
                    turn = 'white'
                    check_free_pieces('white')
                    check_free_locations('white')

        #отмена последнего хода
        if event.type == pygame.MOUSEBUTTONDOWN and 270 <= event.pos[0] <= 330 and 900 <= event.pos[1] <= 960 and not GameOver:
            turn = prev_turn
            black_pieces = copy.deepcopy(prev_black_pieces)
            black_locations = copy.deepcopy(prev_black_locations)
            white_pieces = copy.deepcopy(prev_white_pieces)
            white_locations = copy.deepcopy(prev_white_locations)
            screen.fill((153, 255, 204))
            pygame.draw.rect(screen, (0, 0, 0), (0, 800, 800, 1000))
            draw_board()
            draw_pieces()
            victory_count()
            buttons()
            check_free_pieces(turn)
            check_free_locations(turn)
            pygame.display.flip()

        #активация флажка сдаться
        if event.type == pygame.MOUSEBUTTONDOWN and 370 <= event.pos[0] <= 430 and 900 <= event.pos[1] <= 960 and not GameOver:
            GameOver = True
            if turn == 'white':
                count_black += 1
                game_over('black')
            else:
                count_white += 1
                game_over('white')

        #отмена отмены последнего хода
        if event.type == pygame.MOUSEBUTTONDOWN and 470 <= event.pos[0] <= 530 and 900 <= event.pos[1] <= 960 and not GameOver:
            turn = next_turn
            black_pieces = copy.deepcopy(next_black_pieces)
            black_locations = copy.deepcopy(next_black_locations)
            white_pieces = copy.deepcopy(next_white_pieces)
            white_locations = copy.deepcopy(next_white_locations)
            screen.fill((153, 255, 204))
            pygame.draw.rect(screen, (0, 0, 0), (0, 800, 800, 1000))
            capture(curr_piece_1, curr_piece_2, white_pieces, white_locations)
            capture(curr_piece_1, curr_piece_2, black_pieces, black_locations)
            if turn == 'black':
                white_pieces.append(curr_piece_type)
                white_locations.append(curr_piece_2)
            else:
                black_pieces.append(curr_piece_type)
                black_locations.append(curr_piece_2)
            coronation()
            draw_board()
            draw_pieces()
            victory_count()
            buttons()
            check_free_pieces(turn)
            check_free_locations(turn)
            pygame.display.flip()

        #повторная игра
        if event.type == pygame.KEYDOWN and GameOver:
            reset()


pygame.quit()
