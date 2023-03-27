import pygame
import random

# Инициализация
pygame.init()

info = pygame.display.Info()
WIDTH, HEIGHT = (info.current_w, info.current_h)
is_fullscreen = True

FPS = 60
NAME_GAME = 'Защита Индпро!'

# Параметры игрока
TYPE_CONTROL = None
player_count = None
number_of_player = None


# Параметры всех врагов
ENEMY_COUNT_DIFFICULTY = 30
ENEMY_APPEAR_SPEED = (1620, 3000)  # чем меньше числа, тем быстрее появляется враг (1620, 3000)
BOSS_IN_GAME = False
BOSS_HEALTH = 584
win = False

# Параметры пуль
AMOUNT_BULLET = 3

# Параметры баффов ([1] - доб. Жизнь [2] - доб. макс Пуль [3] - бесконечные пули на некоторое время)
AMOUNT_BUFF = 5
BUFF_CHANCES = [0.40, 0.45, 0.15]

# Списки объектов
enemy_in_game = []
boss_bullets_in_game = []
buffs_in_game = []
PLAYER_LIST = []


# Класс Звезд-декораций
class Star(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.alpha = random.randint(190, 255)

    def flicker(self):
        self.alpha = random.randint(190, 255)
        self.draw()

    def draw(self):
        pygame.draw.circle(screen, (self.alpha, self.alpha, self.alpha), (self.x, self.y), 2)


# Класс Пули
class Bullet(pygame.sprite.Sprite):
    def __init__(self, file_name, x, y, size, speed):
        super().__init__()
        self.size = size
        self.speed = speed
        self.image = pygame.image.load(file_name).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        rand_angle = random.randint(0, 360)
        self.image = pygame.transform.rotate(self.image, rand_angle)
        self.x = x
        self.y = y
        self.rect = pygame.Rect((self.x, self.y), size)

    # Движение пули
    def move(self):
        self.y -= self.speed
        self.rect = pygame.Rect((self.x, self.y), self.size)
        self.draw(screen)

    # Отрисовка пули
    def draw(self, surf):
        surf.blit(self.image, (self.x, self.y))


# класс Баффов
class FallingBuff(pygame.sprite.Sprite):
    def __init__(self, kind):
        super().__init__()
        self.kind = kind

        # Выбор спрайта баффа
        if self.kind == 1:
            self.image = pygame.image.load('img/buff_heart.png').convert_alpha()
        elif self.kind == 2:
            self.image = pygame.image.load('img/buff_bullet.png').convert_alpha()
        elif self.kind == 3:
            self.image = pygame.image.load('img/buff_infinity_bullet.png').convert_alpha()
        else:
            self.image = pygame.image.load('img/button1.png').convert_alpha()

        self.size = WIDTH // 40, WIDTH // 40
        self.image = pygame.transform.scale(self.image, self.size)
        self.x = random.randint(0, WIDTH - self.size[0])
        self.y = 0 - self.size[1]
        self.speed = HEIGHT // 150
        self.rect = pygame.Rect((self.x, self.y), self.size)

    # Движение баффа
    def move(self):
        if self.y < HEIGHT + self.size[1]:
            self.y += self.speed
        self.rect = pygame.Rect((self.x, self.y), self.size)
        self.draw(screen)

    # Отрисовка баффа
    def draw(self, surf):
        surf.blit(self.image, (self.x, self.y))


# класс Кнопок
class Button(pygame.sprite.Sprite):
    def __init__(self, button_passive, button_active, text, x, y, size):
        super().__init__()

        self.x = x
        self.y = y
        self.size = size

        self.image_passive = pygame.transform.scale(button_passive, self.size)
        self.image_active = pygame.transform.scale(button_active, self.size)

        self.image = self.image_passive

        self.rect = pygame.Rect((self.x, self.y), self.size)

        self.text = info_font.render(text, True, 'White')
        self.text_rect = self.text.get_rect(center=(self.size[0]//2 + self.x, self.size[1]//2 + self.y))

    # Обновление кнопки, когда на нее навели
    def update(self, surf):
        mouse = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse):
            self.image = self.image_active
        else:
            self.image = self.image_passive

        self.draw(surf)

    # Проверка нажата ли кнопка
    def is_click(self, event):
        mouse = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONUP:
            return True

    # Отрисовка кнопки
    def draw(self, surf):
        surf.blit(self.image, self.rect)
        surf.blit(self.text, self.text_rect)
        # Рект кнопки
        # pygame.draw.rect(surf, 'Red', self.rect, 2)


# класс Босса
class BossEvent(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.health = BOSS_HEALTH
        self.laser = Laser(temp_player_list[0].x)

        self.size = (WIDTH, 250)
        self.image = pygame.image.load('img/boss.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, self.size)
        self.x = 0
        self.y = -100
        self.max_y = 0
        self.rect = pygame.Rect((self.x, self.y), self.size)

    # Эпичное появление
    def appear(self):
        if self.y < self.max_y:
            self.y += 3
        else:
            self.y = 0
        self.rect = pygame.Rect((self.x, self.y), self.size)

    # Обычная стрельба босса
    def shoot(self):
        if event.type == enemy_timer and not pause:
            random_size = random.randint(WIDTH//40, WIDTH//20)
            bul = Bullet('img/meteorite.png', random.randint(0, WIDTH - random_size), 0, (random_size, random_size),
                         -1 * HEIGHT // 160)
            boss_bullets_in_game.append(bul)
            pygame.time.set_timer(enemy_timer, random.randint(200, 1000))

    # Атака самонаводящимся лазером
    def fire(self, player_x):
        if event.type == enemy_timer_2 and not pause:
            self.laser = Laser(player_x)
            pygame.time.set_timer(enemy_timer_2, random.randint(1500, 3000))

    # Отрисовка босса и его сцены
    def draw(self, surf):
        surf.blit(self.image, (self.x, self.y))
        # Отображение коллайдера
        # pygame.draw.rect(surf, 'Red', self.rect, 2)

        pygame.draw.rect(surf, 'White', (WIDTH//2 - 300, 32, 600, 50), 6)
        pygame.draw.rect(surf, 'Red', (WIDTH//2 - 300 + 8, 39, self.health, 36))
        name_boss = boss_font.render('Гайя', True, 'White')
        name_boss_rect = name_boss.get_rect(center=(WIDTH//2, 20))
        surf.blit(name_boss, name_boss_rect)


# класс Лазера для босса
class Laser(pygame.sprite.Sprite):
    def __init__(self, player_x):
        super().__init__()
        self.current_width, self.current_heigth = (1, 1)
        self.current_size = (self.current_width, self.current_heigth)
        self.width, self.heigth = random.randint(WIDTH//25, WIDTH//15), HEIGHT
        self.size = (self.width, self.heigth)
        self.x = player_x
        self.y = 0
        self.raw_image = pygame.image.load('img/laser.png').convert()
        self.image = pygame.transform.scale(self.raw_image, self.current_size)
        self.rect = pygame.Rect((self.x, self.y), self.current_size)

    def spread(self):
        if self.current_width < self.width:
            self.current_width += 2
            self.x -= 1
        if self.current_heigth < self.heigth:
            self.current_heigth += HEIGHT // 40

        self.current_size = (self.current_width, self.current_heigth)
        self.image = pygame.transform.scale(self.raw_image, self.current_size)
        self.rect = pygame.Rect((self.x, self.y), self.current_size)

    def draw(self, surf):
        surf.blit(self.image, (self.x, self.y))


# Класс Врагов
class Enemy(pygame.sprite.Sprite):
    def __init__(self, kind):
        super().__init__()

        self.kind = kind

        if self.kind == 0:  # Базовый враг
            self.size = (WIDTH // 19, WIDTH // 19)
            self.speed = random.randint(HEIGHT//150, HEIGHT//100)

            self.image = pygame.image.load('img/enemy_basic.png').convert_alpha()
            self.image = pygame.transform.smoothscale(self.image, self.size)

            self.x = random.randint(0, WIDTH - self.size[0])
            self.y = 0 - self.size[0]
        else:  # Угловой враг
            self.size = (WIDTH // 18, WIDTH // 18)
            self.speed = random.randint(HEIGHT//150, HEIGHT//120)
            self.speed_x = random.choice([-1, 1]) * random.uniform(3, 10)

            self.image = pygame.image.load('img/enemy_angle.png').convert_alpha()
            self.image = pygame.transform.smoothscale(self.image, self.size)

            # Поворот спрайта если в противоположную сторону направлен
            if self.speed_x > 0:
                self.image = pygame.transform.flip(self.image, True, False)

            self.y = 0 - self.size[0]

            # Спавн углвого врага в завимости от наклона
            if self.speed_x < 0:
                self.x = random.randint(WIDTH//2, WIDTH-self.size[0])
            else:
                self.x = random.randint(0, WIDTH//2)

        self.rect = pygame.Rect((self.x + 5, self.y + 5), (self.size[0]-10, self.size[1]-10))

    # Движение врага
    def move(self):
        if self.kind == 0:
            if self.y < HEIGHT + self.size[1]:
                self.y += self.speed
        elif self.kind == 1:
            if self.y < HEIGHT + self.size[1] and 0 - self.size[0] < self.x < WIDTH:
                self.y += self.speed
                self.x += self.speed_x
        self.rect = pygame.Rect((self.x + 5, self.y + 5), (self.size[0] - 10, self.size[1] - 10))
        self.draw(screen)

    # Отрисовка врага
    def draw(self, surf):
        surf.blit(self.image, (self.x, self.y))
        # отображение коллайдера
        # pygame.draw.rect(surf, 'Red', self.rect, 2)


# Класс Игрока
class Player(pygame.sprite.Sprite):
    def __init__(self, file_name, type_control):
        pygame.sprite.Sprite.__init__(self)
        self.size = (WIDTH // 13, WIDTH // 13)
        self.speed = WIDTH // 150

        # Выбор спавна игроков
        if number_of_player == 2:
            if player_count == 0:
                self.x = (WIDTH - self.size[0]) // 4
            else:
                self.x = 3 * (WIDTH - self.size[0]) // 4
        else:
            self.x = (WIDTH - self.size[0]) // 2

        self.y = HEIGHT - self.size[1]

        self.image = pygame.image.load(file_name).convert_alpha()
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = pygame.Rect((self.x + 5, self.y + 5), (self.size[0]-10, self.size[1]-10))
        self.kind = type_control
        self.lives = 3
        self.bullet = AMOUNT_BULLET
        self.score = 0
        self.bullets_in_game = []
        self.infinite_bullet = False
        self.time = 0

    # Движение Игрока
    def move(self):
        if self.lives > 0:
            if self.kind == 1:
                key_pressed = pygame.key.get_pressed()
                if key_pressed[pygame.K_d] and self.x < WIDTH - self.size[0]//2:
                    self.x += self.speed
                if key_pressed[pygame.K_a] and self.x > 0 - self.size[0]//2:
                    self.x -= self.speed
            elif self.kind == 2:
                key_pressed = pygame.key.get_pressed()
                if key_pressed[pygame.K_RIGHT] and self.x < WIDTH - self.size[0]//2:
                    self.x += self.speed
                if key_pressed[pygame.K_LEFT] and self.x > 0 - self.size[0]//2:
                    self.x -= self.speed
            elif self.kind == 0:
                self.x = pygame.mouse.get_pos()[0] - self.size[0]//2
            self.rect = pygame.Rect((self.x + 10, self.y + 10), (self.size[0] - 20, self.size[1] - 20))

    # Отрисовка Игрока
    def draw(self, surf):
        if self.lives > 0:
            surf.blit(self.image, (self.x, self.y))
            # отображение коллайдера
            # pygame.draw.rect(surf, 'Red', self.rect, 2)

    # Пиу-пяу
    def shoot(self):

        if (len(self.bullets_in_game) < self.bullet or self.infinite_bullet) and self.lives > 0 and not pause:
            flag = False

            if self.kind == 0 and event.type == pygame.MOUSEBUTTONDOWN:
                flag = True
            elif self.kind == 1 and event.type == pygame.KEYUP and event.key == pygame.K_w:
                flag = True
            elif self.kind == 2 and event.type == pygame.KEYUP and event.key == pygame.K_UP:
                flag = True

            if flag:
                bullet_size = WIDTH // 90, WIDTH // 90
                bullet_speed = HEIGHT // 120
                bul = Bullet('img/bullet.png', self.x + self.size[0] // 2 - bullet_size[0] // 2,
                             self.y + self.size[1] // 2 - bullet_size[1] // 2, bullet_size, bullet_speed)
                self.bullets_in_game.append(bul)
                sound_shoot.play()


# --------- Сцены ------------
def scene_main_menu():
    global running, pause
    global stage
    global number_of_player, player_count, TYPE_CONTROL, PLAYER_LIST
    global boss, BOSS_IN_GAME
    global enemy_in_game, boss_bullets_in_game, buffs_in_game
    global plot
    global is_sound_on
    global screen, WIDTH, HEIGHT

    for star in stars:
        star.flicker()

    # Полноэкранный режим
    if is_fullscreen:
        btn_fullscreen = Button(fullscreen_off_image, fullscreen_off_image, '', WIDTH - WIDTH//30-HEIGHT//40, HEIGHT//40, (WIDTH//30, WIDTH//30))
    else:
        btn_fullscreen = Button(fullscreen_on_image, fullscreen_on_image, '', WIDTH - WIDTH//30-HEIGHT//40, HEIGHT//40, (WIDTH//30, WIDTH//30))

    btn_fullscreen.draw(screen)

    # Звук
    if is_sound_on:
        btn_volume = Button(sound_on_image, sound_on_image, '', WIDTH // 60, HEIGHT // 60, (WIDTH // 25, WIDTH // 25))
    else:
        btn_volume = Button(sound_off_image, sound_off_image, '', WIDTH // 60, HEIGHT // 60, (WIDTH // 25, WIDTH // 25))

    btn_volume.draw(screen)

    text_caption = title_font.render(NAME_GAME, True, 'White')
    text_caption_rect = text_caption.get_rect(center=(WIDTH // 2, 300))

    screen.blit(text_caption, text_caption_rect)

    btn_sizes = (WIDTH//5, HEIGHT//10)
    btn_x = (WIDTH - btn_sizes[0]) // 2
    btn_y = HEIGHT // 2
    btn_offset_y = btn_sizes[1] + HEIGHT // 40

    btn_play_plot = Button(button1_image, button2_image, 'Сюжет', btn_x, btn_y + 0 * btn_offset_y, btn_sizes)
    btn_play_endless = Button(button1_image, button2_image, 'Бесконечный', btn_x, btn_y + 1 * btn_offset_y, btn_sizes)
    btn_exit = Button(button1_image, button2_image, 'Выход', btn_x, btn_y + 2 * btn_offset_y, btn_sizes)

    btn_play_plot.update(screen)
    btn_play_endless.update(screen)
    btn_exit.update(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if btn_play_plot.is_click(event) or btn_play_endless.is_click(event):
            stage += 1
            pause = False
            TYPE_CONTROL = -1
            player_count = 0
            number_of_player = 0
            PLAYER_LIST.clear()

            boss = None
            BOSS_IN_GAME = False

            enemy_in_game.clear()
            boss_bullets_in_game.clear()
            buffs_in_game.clear()

        if btn_play_plot.is_click(event):
            plot = True
        if btn_play_endless.is_click(event):
            plot = False

        if btn_fullscreen.is_click(event) or (event.type == pygame.KEYUP and event.key == pygame.K_F11):
            toggle_fullscreen()

        elif btn_exit.is_click(event):
            running = False

        elif btn_volume.is_click(event):
            toggle_sound()


def scene_sel_number_of_player():
    global running
    global stage
    global number_of_player
    global screen, WIDTH, HEIGHT

    text_chose_number = info_font.render('Сколько игроков', True, 'White')
    text_choose_number_rect = text_chose_number.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    screen.blit(text_chose_number, text_choose_number_rect)

    btn_x = WIDTH // 30
    btn_y = HEIGHT // 2
    btn_sizes = (WIDTH // 2 - 2 * btn_x, HEIGHT // 3)
    btn_offset_x = btn_sizes[0] + 2 * btn_x

    btn_one = Button(button1_image, button2_image, '1 игрок', btn_x + 0 * btn_offset_x, btn_y, btn_sizes)
    btn_two = Button(button1_image, button2_image, '2 игрока', btn_x + 1 * btn_offset_x, btn_y, btn_sizes)

    btn_one.update(screen)
    btn_two.update(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if btn_one.is_click(event):
            number_of_player = 1
            stage += 1
        elif btn_two.is_click(event):
            number_of_player = 2
            stage += 1


def scene_sel_ctrl_type():
    global running, stage
    global player_count, TYPE_CONTROL, number_of_player
    global screen, WIDTH, HEIGHT

    text_player = info_font.render(str(player_count + 1) + ' игрок', True, 'White')
    text_player_rect = text_player.get_rect(center=(WIDTH // 2, HEIGHT // 3 - heigth_font_menu))

    text_choose_type_movement = info_font.render('Выберите тип управления', True, 'White')
    text_choose_type_movement_rect = text_choose_type_movement.get_rect(center=(WIDTH // 2, HEIGHT // 3))

    btn_x = WIDTH // 30
    btn_y = HEIGHT // 2
    btn_sizes = (WIDTH // 3 - btn_x, HEIGHT // 3)
    btn_offset_x = btn_sizes[0] + btn_x // 2

    btn_mouse = Button(button1_image, button2_image, 'Мышка', btn_x + 0 * btn_offset_x, btn_y, btn_sizes)
    btn_ad = Button(button1_image, button2_image, 'Клавиши AD', btn_x + 1 * btn_offset_x, btn_y, btn_sizes)
    btn_arrow = Button(button1_image, button2_image, 'Стрелки', btn_x + 2 * btn_offset_x, btn_y, btn_sizes)

    old_type_control = None
    if player_count == 1:
        old_type_control = PLAYER_LIST[0].kind

    if old_type_control != 0:
        btn_mouse.update(screen)
    if old_type_control != 1:
        btn_ad.update(screen)
    if old_type_control != 2:
        btn_arrow.update(screen)

    screen.blit(text_choose_type_movement, text_choose_type_movement_rect)
    screen.blit(text_player, text_player_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if btn_mouse.is_click(event) and old_type_control != 0:
            TYPE_CONTROL = 0
        elif btn_ad.is_click(event) and old_type_control != 1:
            TYPE_CONTROL = 1
        elif btn_arrow.is_click(event) and old_type_control != 2:
            TYPE_CONTROL = 2

        if TYPE_CONTROL != -1:
            player = Player('img/player_' + str(player_count + 1) + '.png', TYPE_CONTROL)
            PLAYER_LIST.append(player)
            player_count += 1

            if player_count == number_of_player:
                stage += 1
                break
            else:
                TYPE_CONTROL = -1


def cut_scene(end):
    global stage
    global running
    global count_cut

    # Фон катсцены
    bg_cut_scene = pygame.transform.scale(cut_scene_image[count_cut-1], (HEIGHT*1.7778, HEIGHT))
    bg_cut_scene_rect = bg_cut_scene.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(bg_cut_scene, bg_cut_scene_rect)

    # Полупрозрачный прямоугольник
    alpha = pygame.Surface((WIDTH - 50, HEIGHT // 5))
    alpha.set_alpha(128)
    alpha.fill('White')
    alpha_rect = alpha.get_rect(midbottom=(WIDTH // 2, HEIGHT - 10))
    screen.blit(alpha, alpha_rect)

    # Текст катсцены
    text = cs_text[count_cut-1]
    words = text.split(' ')
    lines = []
    current_line = words[0]
    for word in words[1::]:
        if cut_font.size(current_line + ' ' + word)[0] < WIDTH - 100:
            current_line += ' ' + word
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)

    for (i, line) in enumerate(lines):
        rendered = cut_font.render(line, True, 'Black')
        screen.blit(rendered, (50, 4 * HEIGHT // 5 + i * heigth_font_cs))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE or event.type == pygame.MOUSEBUTTONUP:
            count_cut += 1
            if count_cut > end:
                stage += 1
                if stage == 4:
                    pygame.mixer.music.load('music/background.ogg')
                    pygame.mixer.music.play(-1)
                if len(PLAYER_LIST) == 1:
                    count_cut += 1


def scene_pause():
    global running, pause
    global stage, count_cut
    global WIDTH, HEIGHT, screen

    # Все возможные отрисовки
    if buffs_in_game:
        for entity in buffs_in_game:
            entity.draw(screen)

    for pl in PLAYER_LIST:
        if pl.bullets_in_game:
            for entity in pl.bullets_in_game:
                entity.draw(screen)
        pl.draw(screen)

    if boss_bullets_in_game:
        for entity in boss_bullets_in_game:
            entity.draw(screen)

    if enemy_in_game:
        for entity in enemy_in_game:
            entity.draw(screen)
    if boss:
        boss.laser.draw(screen)
        boss.draw(screen)

    pygame.mixer.music.pause()

    # Установка видимого курсора
    pygame.mouse.set_visible(True)

    # Полупрозрачный прямоугольник
    alpha = pygame.Surface((WIDTH - 50, HEIGHT - 50))
    alpha.set_alpha(64)
    alpha.fill((255, 255, 255))
    alpha_rect = alpha.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(alpha, alpha_rect)

    # Звук
    if is_sound_on:
        btn_volume = Button(sound_on_image, sound_on_image, '', WIDTH // 60, HEIGHT // 60, (WIDTH // 25, WIDTH // 25))
    else:
        btn_volume = Button(sound_off_image, sound_off_image, '', WIDTH // 60, HEIGHT // 60, (WIDTH // 25, WIDTH // 25))

    btn_volume.draw(screen)

    text_pause = info_font.render('Пауза', True, 'White')
    text_pause_rect = text_pause.get_rect(center=(WIDTH // 2, HEIGHT // 3))

    screen.blit(text_pause, text_pause_rect)

    btn_sizes = (WIDTH // 5, HEIGHT // 10)
    btn_x = (WIDTH - btn_sizes[0]) // 2
    btn_y = HEIGHT // 2
    btn_offset_y = btn_sizes[1] + HEIGHT // 40

    btn_continue = Button(button1_image, button2_image, 'Продолжить', btn_x, btn_y + 0 * btn_offset_y, btn_sizes)
    btn_main_menu = Button(button1_image, button2_image, 'Главное меню', btn_x, btn_y + 1 * btn_offset_y, btn_sizes)
    btn_exit = Button(button1_image, button2_image, 'Выход', btn_x, btn_y + 2 * btn_offset_y, btn_sizes)

    btn_continue.update(screen)
    btn_main_menu.update(screen)
    btn_exit.update(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if btn_continue.is_click(event) or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
            pygame.mixer.music.unpause()
            pause = False
        elif btn_exit.is_click(event):
            running = False
        elif btn_main_menu.is_click(event):
            stage = 0
            count_cut = 1
            pygame.mixer.music.load('music/main_menu.mp3')
            pygame.mixer.music.play(-1)
        elif btn_volume.is_click(event):
            toggle_sound()

# -----------------------------


# ---------- Функции ----------
def is_game():
    flag = False
    for pl in PLAYER_LIST:
        if pl.lives > 0:
            flag = True
    return flag


def toggle_sound():
    global is_sound_on
    if is_sound_on:
        is_sound_on = False
        pygame.mixer.music.set_volume(0)
    else:
        is_sound_on = True
        pygame.mixer.music.set_volume(0.2)


def toggle_fullscreen():
    global is_fullscreen, WIDTH, HEIGHT
    global screen
    global heigth_font_menu, info_font, info_font_underline, boss_font, cut_font, title_font, heigth_font_title
    global background, stars

    if is_fullscreen:
        WIDTH, HEIGHT = (1280, 720)
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        is_fullscreen = False
    else:
        WIDTH, HEIGHT = (info.current_w, info.current_h)
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        is_fullscreen = True

    # Список для хранения координат звезд в главном меню
    stars = []

    # Создание списка звезд
    for i in range(50):
        star = Star(random.randint(0, WIDTH), random.randint(0, HEIGHT))
        stars.append(star)

    # Настройка текста
    heigth_font_menu = HEIGHT // 35
    heigth_font_cs = HEIGHT // 30
    heigth_font_title = HEIGHT // 20
    cut_font = pygame.font.Font('fonts/Jura-VariableFont_wght.ttf', heigth_font_cs)
    info_font = pygame.font.Font('fonts/Marske.ttf', heigth_font_menu)
    info_font_underline = pygame.font.Font('fonts/Marske.ttf', heigth_font_menu)
    info_font_underline.set_underline(True)
    boss_font = pygame.font.Font('fonts/New Zelek.ttf', heigth_font_menu)
    title_font = pygame.font.Font('fonts/Researchremix-1nje.otf', heigth_font_title)

    background = pygame.transform.scale(background, (WIDTH, WIDTH * 2.25))

# -----------------------------


# Настройка игры
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption(NAME_GAME)
icon = pygame.image.load('img/player_1.png').convert_alpha()
pygame.display.set_icon(icon)

# Настройка часов
clock = pygame.time.Clock()
enemy_timer = pygame.USEREVENT + 1
enemy_timer_2 = pygame.USEREVENT + 2
pygame.time.set_timer(enemy_timer, random.randint(ENEMY_APPEAR_SPEED[0], ENEMY_APPEAR_SPEED[1]))
pygame.time.set_timer(enemy_timer_2, random.randint(ENEMY_APPEAR_SPEED[0], ENEMY_APPEAR_SPEED[1]))
start_ticks = None


# Настройка музыки
sound_shoot = pygame.mixer.Sound('music/sound_shoot.mp3')
sound_shoot.set_volume(0.5)
sound_death_enemy = pygame.mixer.Sound('music/sound_enemy_death.mp3')
sound_death_enemy.set_volume(0.8)
sound_injury_player = pygame.mixer.Sound('music/sound_injury.mp3')
sound_injury_player.set_volume(0.5)
sound_buff_bullet = pygame.mixer.Sound('music/sound_buff_bullet.mp3')
sound_buff_bullet.set_volume(0.5)
sound_buff_heart = pygame.mixer.Sound('music/sound_buff_heart.mp3')
sound_buff_heart.set_volume(0.5)
pygame.mixer.music.load('music/main_menu.mp3')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)
is_sound_on = True

# Настройка текста
heigth_font_menu = HEIGHT // 30
heigth_font_cs = HEIGHT // 30
heigth_font_title = HEIGHT // 20

cut_font = pygame.font.Font('fonts/Jura-VariableFont_wght.ttf', heigth_font_cs)
info_font = pygame.font.Font('fonts/Marske.ttf', heigth_font_menu)
info_font_underline = pygame.font.Font('fonts/Marske.ttf', heigth_font_menu)
info_font_underline.set_underline(True)
boss_font = pygame.font.Font('fonts/New Zelek.ttf', heigth_font_menu)
title_font = pygame.font.Font('fonts/Researchremix-1nje.otf', heigth_font_title)

# Загрузка некоторых изображений (ради оптимизации некоторых моментов)
background = pygame.image.load('img/background.png').convert()
background = pygame.transform.scale(background, (WIDTH, WIDTH * 2.25))

button1_image = pygame.image.load('img/button1.png').convert_alpha()
button2_image = pygame.image.load('img/button2.png').convert_alpha()

fullscreen_off_image = pygame.image.load('img/fullscreen_off.png').convert_alpha()
fullscreen_on_image = pygame.image.load('img/fullscreen_on.png').convert_alpha()

sound_off_image = pygame.image.load('img/sound_off.png').convert_alpha()
sound_on_image = pygame.image.load('img/sound_on.png').convert_alpha()

cut_scene_image = []
for i in range(12):
    cut_scene_image.append(pygame.image.load('img/cs' + str(i+1) + '.png').convert())

# Вспомогательные переменные, которые возможно нужны
kind_buff = 0
pause = False
plot = False
boss = None
count_cut = 1
background_pos = 0

# Счетчик сцен (0 - Главное меню; 1 - Выбор количества игроков; 2 - Выбор управления; 3 - Катсцена; 4 - Игровое поле; 5 - Финальная катсцена; 6 - Фин)
stage = 0

# Чтение катсцен
with open('text/cutscene.txt', 'r', encoding='UTF-8') as cs:
    cs_text = [line.strip() for line in cs.readlines()]

# Чтение рекорда
file_record = open('text/high_record.txt', 'r')
record = int(file_record.readline())
file_record.close()

# Список для хранения координат звезд в главном меню
stars = []

# Создание списка звезд
for i in range(50):
    star = Star(random.randint(0, WIDTH), random.randint(0, HEIGHT))
    stars.append(star)


# Основной цикл игры
running = True
while running:
    # Вывод фпс игры
    # print(clock.get_fps())

    clock.tick(FPS)

    screen.fill('#101331')

    # Главное меню
    if stage == 0:
        scene_main_menu()

    # Выбор количества игроков
    elif stage == 1:
        scene_sel_number_of_player()

    # Выбор управления
    elif stage == 2:
        scene_sel_ctrl_type()

    # Катсцена
    elif stage == 3:
        if plot:
            cut_scene(7 + len(PLAYER_LIST)-1)
        else:
            stage += 1
            pygame.mixer.music.load('music/background.ogg')
            pygame.mixer.music.play(-1)

    # Игровое поле
    elif stage == 4:
        if is_game():
            # Динамичный фон
            screen.blit(background, (0, background_pos))
            screen.blit(background, (0, background_pos - WIDTH * 2.25))
            if not pause:
                background_pos += 3
                if background_pos >= WIDTH * 2.25:
                    background_pos = 0

            # Создание перемешанного списка ради разрешения конфликтных ситуаций в мультиплеере
            temp_player_list = PLAYER_LIST.copy()
            random.shuffle(temp_player_list)
            if temp_player_list[0].lives <= 0:
                temp = temp_player_list[0]
                temp_player_list[0] = temp_player_list[1]
                temp_player_list[1] = temp

            # Пауза
            if pause:
                scene_pause()

            # Не пауза
            else:

                # Ивенты
                for event in pygame.event.get():

                    # Закрытие игры
                    if event.type == pygame.QUIT:
                        running = False

                    # Пауза по нажатию кнопки
                    if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                        pause = True
                        break

                    # Пауза, когда экран не в фокусе
                    if event.type == pygame.ACTIVEEVENT:
                        if event.state == 2:
                            pause = True
                            break

                    # Спавн врагов (в класс?)
                    if not BOSS_IN_GAME and event.type == enemy_timer and len(enemy_in_game) < ENEMY_COUNT_DIFFICULTY and not pause:
                        kind_enemy = random.randint(0, 1)
                        enemy = Enemy(kind_enemy)
                        enemy_in_game.append(enemy)

                        # Спавн врагов в зависимости от максимального количества очков
                        max_score = 0
                        for pl in PLAYER_LIST:
                            if pl.score >= max_score:
                                max_score = pl.score
                        if ENEMY_APPEAR_SPEED[0] - 20 * max_score <= 0:
                            if plot:
                                if not BOSS_IN_GAME:
                                    BOSS_IN_GAME = True
                                    pygame.mixer.music.load('music/boss_theme.mp3')
                                    pygame.mixer.music.play(-1)
                            else:
                                pygame.time.set_timer(enemy_timer, random.randint(1, 750))

                        else:
                            pygame.time.set_timer(enemy_timer, random.randint(ENEMY_APPEAR_SPEED[0] - 20 * max_score,
                                                                              ENEMY_APPEAR_SPEED[1] - 30 * max_score))

                    if BOSS_IN_GAME and not boss and len(enemy_in_game) == 0:
                        boss = BossEvent()

                    # Стрельба игрока
                    for entity in PLAYER_LIST:
                        entity.shoot()

                    # Атаки босса
                    if boss:
                        if 2 * BOSS_HEALTH // 3 < boss.health:
                            boss.shoot()
                        elif BOSS_HEALTH // 3 < boss.health < 2 * BOSS_HEALTH // 3:
                            boss.fire(temp_player_list[0].x + temp_player_list[0].size[0] // 2)
                        else:
                            boss.shoot()
                            boss.fire(temp_player_list[0].x + temp_player_list[0].size[0] // 2)

                # Невидимость курсора
                pygame.mouse.set_visible(False)

                # Отрисовка и столкновения баффов (в класс?)
                if buffs_in_game:
                    for entity in list(buffs_in_game):
                        entity.move()

                        if entity.y > HEIGHT:
                            buffs_in_game.remove(entity)

                        for pl in temp_player_list:
                            if pl.rect.colliderect(entity.rect):
                                if entity in buffs_in_game:
                                    buffs_in_game.remove(entity)
                                    if entity.kind == 1:
                                        pl.lives += 1
                                        sound_buff_heart.play()
                                    elif entity.kind == 2:
                                        pl.bullet += 1
                                        sound_buff_bullet.play()
                                    elif entity.kind == 3:
                                        pl.time = pygame.time.get_ticks()
                                        pl.infinite_bullet = True
                                        sound_buff_bullet.play()

                # Отрисовка игрока
                for pl in PLAYER_LIST:  # Берется не перемешанный список, чтобы не было мерцания на экране
                    if pl.bullets_in_game:
                        for entity in list(pl.bullets_in_game):
                            entity.move()
                            if entity.y < 0:
                                pl.bullets_in_game.remove(entity)
                    pl.move()
                    pl.draw(screen)

                # Отрисовка, столкновения врагов и генераци Баффов
                if enemy_in_game:
                    for entity in list(enemy_in_game):
                        entity.move()

                        if entity.y > HEIGHT or not (0 - entity.size[0] < entity.x < WIDTH):  # Удаление врага за границы экрана
                            enemy_in_game.remove(entity)

                        for pl in temp_player_list:  # Столконовение игрока с врагом
                            if pl.rect.colliderect(entity.rect) and pl.lives > 0:
                                if entity in enemy_in_game:
                                    enemy_in_game.remove(entity)
                                    pl.lives -= 1
                                    sound_injury_player.play()

                            elif pl.bullets_in_game:  # Столкновение пули игрока с врагом
                                for bullet in list(pl.bullets_in_game):
                                    if bullet.rect.colliderect(entity.rect):
                                        if entity in enemy_in_game:
                                            enemy_in_game.remove(entity)
                                            pl.bullets_in_game.remove(bullet)
                                            if entity.kind == 0:
                                                pl.score += 1
                                            else:
                                                pl.score += 3
                                            sound_death_enemy.play()

                                        # Спавн Баффов
                                        if not pl.infinite_bullet:
                                            chance_buff = random.random()
                                            if len(buffs_in_game) < AMOUNT_BUFF:
                                                if chance_buff < 0.1:
                                                    buff_names = ['Heart', 'Bullet', 'Inf']
                                                    act = random.choices(buff_names, BUFF_CHANCES)[0]
                                                    if act == 'Inf':
                                                        kind_buff = 3
                                                    elif act == 'Heart':
                                                        kind_buff = 1
                                                    elif act == 'Bullet':
                                                        kind_buff = 2

                                                    if kind_buff != 0:
                                                        buff = FallingBuff(kind_buff)
                                                        buffs_in_game.append(buff)
                                                        kind_buff = 0

                # Отрисовка пуль босса
                if boss_bullets_in_game:
                    for entity in list(boss_bullets_in_game):
                        entity.move()
                        if entity.y > HEIGHT + entity.size[1]:
                            boss_bullets_in_game.remove(entity)

                        for pl in temp_player_list:
                            if entity.rect.colliderect(pl.rect) and pl.lives > 0:
                                if entity in boss_bullets_in_game:
                                    boss_bullets_in_game.remove(entity)
                                    pl.lives -= 1
                                    sound_injury_player.play()

                if boss:
                    boss.appear()
                    if boss.health < 2 * BOSS_HEALTH // 3:
                        boss.laser.spread()
                        boss.laser.draw(screen)
                    boss.draw(screen)
                    for pl in temp_player_list:
                        if pl.bullets_in_game:
                            for entity in list(pl.bullets_in_game):
                                if entity.rect.colliderect(boss.rect):
                                    pl.bullets_in_game.remove(entity)
                                    boss.health -= 5
                        if boss.health < 2 * BOSS_HEALTH // 3:
                            if boss.laser.rect.colliderect(pl.rect) and pl.lives > 0:
                                pl.lives -= 1
                                sound_injury_player.play()

                    if boss.health <= 0:
                        for pl in temp_player_list:
                            win = True
                            pl.lives = 0

                # Надписи на экране
                for (i, pl) in enumerate(PLAYER_LIST):  # Чтоб не было мерцания берем упорядоченный список
                    info_player = info_font_underline.render(str(i + 1) + ' игрок', True, 'White')
                    if pl.lives > 0:
                        info_life = info_font.render('Жизни ' + str(pl.lives), True, 'White')
                        info_score = info_font.render('Очки ' + str(pl.score), True, 'White')
                        if pl.infinite_bullet:
                            info_bullet = info_font.render('Пули inf', True, 'White')
                            seconds = (pygame.time.get_ticks()-pl.time)/1000
                            info_timer_infinity = info_font.render('00 0' + str(round(10 - seconds) - 1), True, 'Red')
                            if i == 0:
                                info_timer_infinity_rect = info_timer_infinity.get_rect(topleft=(0, 4 * heigth_font_menu))
                            else:
                                info_timer_infinity_rect = info_timer_infinity.get_rect(topright=(WIDTH, 4 * heigth_font_menu))
                            screen.blit(info_timer_infinity, info_timer_infinity_rect)
                            if seconds >= 9:
                                pl.infinite_bullet = False
                        else:
                            if pl.bullet - len(pl.bullets_in_game) <= 0:
                                info_bullet = info_font.render('Пули 0', True, 'White')
                            else:
                                info_bullet = info_font.render('Пули ' + str(pl.bullet - len(pl.bullets_in_game)), True, 'White')
                    else:
                        info_life = info_font.render('Жизни 0', True, 'White')
                        info_score = info_font.render('Очки ' + str(pl.score), True, 'White')
                        info_bullet = info_font.render('Пули 0', True, 'White')

                    if i == 0:
                        info_player_rect = info_player.get_rect(topleft=(0, 0 * heigth_font_menu))
                        info_life_rect = info_life.get_rect(topleft=(0, 1 * heigth_font_menu))
                        info_bullet_rect = info_bullet.get_rect(topleft=(0, 2 * heigth_font_menu))
                        info_score_rect = info_score.get_rect(topleft=(0, 3 * heigth_font_menu))

                        # pygame.draw.line(screen, 'White', (0, heigth_font + 5), (100, heigth_font + 5), HEIGHT // 250)
                    else:
                        info_player_rect = info_player.get_rect(topright=(WIDTH, 0 * heigth_font_menu))
                        info_life_rect = info_life.get_rect(topright=(WIDTH, 1 * heigth_font_menu))
                        info_bullet_rect = info_bullet.get_rect(topright=(WIDTH, 2 * heigth_font_menu))
                        info_score_rect = info_score.get_rect(topright=(WIDTH, 3 * heigth_font_menu))

                        # pygame.draw.line(screen, 'White', (WIDTH-100, heigth_font + 5), (WIDTH, heigth_font + 5), HEIGHT // 250)

                    screen.blit(info_player, info_player_rect)
                    screen.blit(info_life, info_life_rect)
                    screen.blit(info_bullet, info_bullet_rect)
                    screen.blit(info_score, info_score_rect)

        # Переключение сцены
        else:
            stage += 1
            pygame.mixer.music.load('music/main_menu.mp3')
            pygame.mixer.music.play(-1)

    # Финальная катсцена
    elif stage == 5:
        # Установка видимого курсора
        pygame.mouse.set_visible(True)

        if plot and win:
            cut_scene(11 + len(PLAYER_LIST)-1)
        else:
            stage += 1

    # Экран проигрыша/выигрыша
    elif stage == 6:
        if not plot:
            max_score = 0
            winner = -1
            for (el, pl) in enumerate(PLAYER_LIST):
                if pl.score > max_score:
                    max_score = pl.score
                    if winner == el:
                        winner = 3
                        break
                    winner = el

            if max_score > record:  # Запись рекорда в файл
                file_record = open('text/high_record.txt', 'w')
                record = max_score
                file_record.write(str(record))
                file_record.close()

            if len(PLAYER_LIST) == 2:
                if winner != -1:
                    text_winner = info_font.render('Победитель Игрок ' + str(winner + 1), True, 'White')
                    text_winner_rect = text_winner.get_rect(center=(WIDTH//2, HEIGHT//2 - 100))
                    screen.blit(text_winner, text_winner_rect)
                else:
                    text_winner = info_font.render('Победила Дружба', True, 'White')
                    text_winner_rect = text_winner.get_rect(center=(WIDTH//2, HEIGHT//2 - 100))
                    screen.blit(text_winner, text_winner_rect)

            text_record = info_font.render('Рекорд ' + str(record), True, 'White')
            screen.blit(text_record, (0, 24))

        if win and plot:
            text_death = info_font.render('Победа', True, 'White')
        else:
            text_death = info_font.render('Проигрыш', True, 'White')

        text_death_rect = text_death.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        screen.blit(text_death, text_death_rect)

        btn_sizes = (WIDTH // 5, HEIGHT // 10)
        btn_x = (WIDTH - btn_sizes[0]) // 2
        btn_y = HEIGHT // 2
        btn_offset_y = btn_sizes[1] + HEIGHT // 40

        btn_retry = Button(button1_image, button2_image, 'Заново', btn_x, btn_y + 0 * btn_offset_y, btn_sizes)
        btn_retry.update(screen)

        btn_main_menu = Button(button1_image, button2_image, 'Главное меню', btn_x, btn_y + 1 * btn_offset_y, btn_sizes)
        btn_main_menu.update(screen)

        btn_exit = Button(button1_image, button2_image, 'Выход', btn_x, btn_y + 2 * btn_offset_y, btn_sizes)
        btn_exit.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if btn_retry.is_click(event):
                stage = 4
                record = None

                count_cut = 9

                if boss:
                    boss = None
                BOSS_IN_GAME = False

                enemy_in_game.clear()
                boss_bullets_in_game.clear()
                buffs_in_game.clear()

                pygame.mixer.music.load('music/background.ogg')
                pygame.mixer.music.play(-1)

                ctrl_player = []
                player_count = 0
                for pl in PLAYER_LIST:
                    ctrl_player.append(pl.kind)
                PLAYER_LIST.clear()
                for pl in range(len(ctrl_player)):
                    player = Player('img/player_'+str(pl+1)+'.png', ctrl_player[pl])
                    PLAYER_LIST.append(player)
                    player_count += 1

            elif btn_main_menu.is_click(event):
                stage = 0
                count_cut = 1

            elif btn_exit.is_click(event):
                running = False

    pygame.display.update()

pygame.quit()
