import pygame
import random


# Инициализация
pygame.init()

# Параметры экрана
WIDTH = 800
HEIGHT = 600
FPS = 60
NAME_GAME = 'Shoot in space'

# Параметры игрока
PLAYER_SIZE = (80, 80)
PLAYER_SPEED = 6
PLAYER_X, PLAYER_Y = (WIDTH - PLAYER_SIZE[0]) // 2, HEIGHT - PLAYER_SIZE[1]
LIVES = 300
SCORE = 0
TYPE_CONTROL = -1
player_count = 0
number_of_player = 0

# Параметры базового врага (0)
BASIC_ENEMY_SIZE = (50, 50)
BASIC_ENEMY_SPEED = (3, 5)

# Параметры углового врага (1)
ANGLE_ENEMY_SIZE = (60, 60)
ANGLE_ENEMY_SPEED = (4, 5)

# Параметры всех врагов
ENEMY_COUNT_DIFFICULTY = 15
ENEMY_APPEAR_SPEED = (500, 1000)  # чем меньше числа, тем быстрее появляется враг (1500, 3000)
BOSS_IN_GAME = False
BOSS_HEALTH = 584

# Параметры пуль
BULLET_SIZE = (10, 10)
BULLET_SPEED = 5
AMOUNT_BULLET = 300

# Параметры баффов ([1] - доб. Жизнь [2] - доб. макс Пуль [3] - бесконечные пули на некоторое время)
BUFF_SIZE = (20, 20)
BUFF_SPEED = 4
BUFF_AMOUNT = 5
BUFF_CHANCE_1 = 0.95  # 0.95
BUFF_CHANCE_2 = 0.93  # 0.93
BUFF_CHANCE_3 = 0.99  # 0.99

# Списки объектов
enemy_in_game = []
boss_bullets_in_game = []
buffs_in_game = []
PLAYER_LIST = []


# Класс Пули
class Bullet(pygame.sprite.Sprite):
    def __init__(self, file_name, x, y, size, speed):
        super().__init__()
        self.size = size
        self.speed = speed
        self.image = pygame.image.load(file_name).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.x = x
        self.y = y
        self.rect = pygame.Rect((self.x, self.y), size)

    # Движение пули
    def move(self):
        if 0 - self.size[1] < self.y < HEIGHT:
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

        self.image = pygame.transform.scale(self.image, BUFF_SIZE)
        self.size = BUFF_SIZE
        self.x = random.randint(0, WIDTH - self.size[0])
        self.y = 0 - self.size[1]
        self.speed = BUFF_SPEED
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
    def __init__(self, file_name_passive, file_name_active, text, x, y, size):
        super().__init__()

        self.x = x
        self.y = y
        self.size = size

        self.image_passive = pygame.image.load(file_name_passive).convert_alpha()
        self.image_passive = pygame.transform.scale(self.image_passive, size)

        self.image_active = pygame.image.load(file_name_active).convert_alpha()
        self.image_active = pygame.transform.scale(self.image_active, size)

        self.image = self.image_passive

        self.rect = pygame.Rect((self.x, self.y), size)

        self.text = info_text.render(text, True, 'White')
        self.text_rect = self.text.get_rect(center=(self.size[0]//2 + self.x, self.size[1]//2 + self.y))

    # Обновление кнопки, когда на нее навели
    def update(self, surf):
        mouse = pygame.mouse.get_pos()

        if self.x <= mouse[0] <= self.size[0] + self.x and self.y <= mouse[1] <= self.size[1] + self.y:
            self.image = self.image_active
        else:
            self.image = self.image_passive

        self.draw(surf)

    # Проверка нажата ли кнопка
    def is_click(self, event):
        if self.rect.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONUP:
            return True

    # Отрисовка кнопки
    def draw(self, surf):
        surf.blit(self.image, (self.x, self.y))
        surf.blit(self.text, self.text_rect)


# класс Босса
class BossEvent(pygame.sprite.Sprite):
    def __init__(self, file_name):
        super().__init__()
        self.x = 0
        self.y = -80
        self.size = (WIDTH, 250)
        self.image = pygame.image.load(file_name).convert_alpha()
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = pygame.Rect((self.x, self.y), self.size)
        self.rect_laser = None

    # Обычная стрельба босса
    def shoot(self):
        if event.type == enemy_timer and not pause:
            bul = Bullet('img/enemy_basic.png', random.randint(0, WIDTH - BULLET_SIZE[0]), 0, BULLET_SIZE, -1 * BULLET_SPEED)
            boss_bullets_in_game.append(bul)
            sound_shoot.play()
            pygame.time.set_timer(enemy_timer, random.randint(100, 5000))

    # На разработке (до появление лазера поялвяется счетчик, игроку надо спрятаться, иначе не хило так продамажет)
    def fire(self):
        if event.type == enemy_timer and not pause and random.randint(1, 100) <= 100:
            print('ПИУ ПЯУ')
            pygame.time.set_timer(enemy_timer, random.randint(100, 5000))

    # Отрисовка босса и его сцены
    def draw(self, surf, health):
        surf.blit(self.image, (self.x, self.y))
        pygame.draw.rect(surf, 'White', (WIDTH//2 - 300, 17, 600, 50), 8)
        pygame.draw.rect(surf, 'Red', (WIDTH//2 - 300 + 8, 24, health, 36))
        name_boss = info_text.render('Гайя', True, 'White')
        name_boss_rect = name_boss.get_rect(center=(WIDTH//2, 7))
        surf.blit(name_boss, name_boss_rect)


# Класс Врагов
class Enemy(pygame.sprite.Sprite):
    def __init__(self, kind):
        super().__init__()

        self.kind = kind

        if self.kind == 0:
            self.size = BASIC_ENEMY_SIZE
            self.speed = random.randint(BASIC_ENEMY_SPEED[0], BASIC_ENEMY_SPEED[1])

            self.image = pygame.image.load('img/enemy_basic.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, self.size)

            self.x = random.randint(0, WIDTH - self.size[0])
            self.y = 0 - self.size[0]
        else:
            self.size = ANGLE_ENEMY_SIZE
            self.speed = random.randint(ANGLE_ENEMY_SPEED[0], ANGLE_ENEMY_SPEED[1])
            self.speed_x = random.choice([-1, 1]) * random.uniform(3, 10)

            self.image = pygame.image.load('img/enemy_angle.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, self.size)

            # Поворот спрайта если в противоположную сторону направлен
            if self.speed_x < 0:
                self.image = pygame.transform.flip(self.image, True, False)

            self.y = 0 - self.size[0]

            # Спавн углвого врага в завимости от наклона
            if self.speed_x < 0:
                self.x = random.randint(WIDTH//2, WIDTH-self.size[0])
            else:
                self.x = random.randint(0, WIDTH//2)

        self.rect = pygame.Rect((self.x, self.y), self.size)

    # Движение врага
    def move(self):
        if self.kind == 0:
            if self.y < HEIGHT + self.size[1]:
                self.y += self.speed
        elif self.kind == 1:
            if self.y < HEIGHT + self.size[1] and 0 - self.size[0] < self.x < WIDTH:
                self.y += self.speed
                self.x += self.speed_x
        self.rect = pygame.Rect((self.x, self.y), self.size)
        self.draw(screen)

    # Отрисовка врага
    def draw(self, surf):
        surf.blit(self.image, (self.x, self.y))


# Класс Игрока
class Player(pygame.sprite.Sprite):
    def __init__(self, file_name, type_control):
        pygame.sprite.Sprite.__init__(self)
        self.size = PLAYER_SIZE
        self.speed = PLAYER_SPEED

        # Выбор спавна игроков
        if number_of_player == 2:
            if player_count == 0:
                self.x = PLAYER_X // 2
                self.y = PLAYER_Y
            else:
                self.x = 3 * PLAYER_X // 2
                self.y = PLAYER_Y
        else:
            self.x = PLAYER_X
            self.y = PLAYER_Y

        self.image = pygame.image.load(file_name).convert_alpha()
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = pygame.Rect((self.x, self.y), self.size)
        self.kind = type_control
        self.lives = LIVES
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
                if key_pressed[pygame.K_d] and self.x < WIDTH - self.size[0]:
                    self.x += self.speed
                if key_pressed[pygame.K_a] and self.x > 0:
                    self.x -= self.speed
            elif self.kind == 2:
                key_pressed = pygame.key.get_pressed()
                if key_pressed[pygame.K_RIGHT] and self.x < WIDTH - self.size[0]:
                    self.x += self.speed
                if key_pressed[pygame.K_LEFT] and self.x > 0:
                    self.x -= self.speed
            elif self.kind == 0:
                self.x = pygame.mouse.get_pos()[0] - self.size[0]//2
            self.rect = pygame.Rect((self.x, self.y), self.size)

    # Отрисовка Игрока
    def draw(self, surf):
        if self.lives > 0:
            surf.blit(self.image, (self.x, self.y))

    # Пиу-пяу
    def shoot(self):

        if (len(self.bullets_in_game) < self.bullet or self.infinite_bullet) and self.lives > 0:
            flag = False

            if self.kind == 0 and event.type == pygame.MOUSEBUTTONDOWN:
                flag = True
            elif self.kind == 1 and event.type == pygame.KEYUP and event.key == pygame.K_w:
                flag = True
            elif self.kind == 2 and event.type == pygame.KEYUP and event.key == pygame.K_UP:
                flag = True

            if flag:
                bul = Bullet('img/bullet.png', self.x + self.size[0] // 2 - BULLET_SIZE[0] // 2,
                             self.y + self.size[1] // 2 - BULLET_SIZE[1] // 2, BULLET_SIZE, BULLET_SPEED)
                self.bullets_in_game.append(bul)
                sound_shoot.play()


# --------- Сцены ------------
def scene_main_menu():
    global running
    global stage

    text_caption = info_text.render(NAME_GAME, True, 'White')
    text_caption_rect = text_caption.get_rect(center=(WIDTH // 2, 200))

    screen.blit(text_caption, text_caption_rect)

    btn_play = Button('img/button1.png', 'img/button2.png', 'Играть', WIDTH // 2 - 75, HEIGHT // 2, (150, 100))
    btn_exit = Button('img/button1.png', 'img/button2.png', 'Выход', WIDTH // 2 - 75, HEIGHT // 2 + 100, (150, 100))

    btn_play.update(screen)
    btn_exit.update(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if btn_play.is_click(event):
            stage += 1
        elif btn_exit.is_click(event):
            running = False


def scene_sel_number_of_player():
    global running
    global stage
    global number_of_player

    text_chose_number = info_text.render('Сколько игроков?', True, 'White')
    text_choose_number_rect = text_chose_number.get_rect(center=(WIDTH // 2, 200))
    screen.blit(text_chose_number, text_choose_number_rect)

    btn_one = Button('img/button1.png', 'img/button2.png', '1 игрок', 10, 150, (WIDTH // 2 - 20, 500))
    btn_two = Button('img/button1.png', 'img/button2.png', '2 игрока', WIDTH // 2 + 10, 150, (WIDTH // 2 - 20, 500))

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
    global running
    global player_count
    global stage
    global TYPE_CONTROL
    global number_of_player

    text_player = info_text.render(str(player_count + 1) + ' игрок', True, 'White')
    text_player_rect = text_player.get_rect(center=(WIDTH//2, 150))

    text_choose_type_movement = info_text.render('Выберите тип управления: ', True, 'White')
    text_choose_type_movement_rect = text_choose_type_movement.get_rect(center=(WIDTH // 2, 200))

    btn_mouse = Button('img/button1.png', 'img/button2.png', 'Мышка', 10, HEIGHT // 2, (250, 200))
    btn_ad = Button('img/button1.png', 'img/button2.png', 'Клавиши AD', WIDTH // 2 - 125, HEIGHT // 2, (250, 200))
    btn_arrow = Button('img/button1.png', 'img/button2.png', 'Стрелки', WIDTH - 260, HEIGHT // 2, (250, 200))

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
        if btn_ad.is_click(event) and old_type_control != 1:
            TYPE_CONTROL = 1
        if btn_arrow.is_click(event) and old_type_control != 2:
            TYPE_CONTROL = 2

        if TYPE_CONTROL != -1:
            player = Player('img/player_' + str(player_count + 1) + '.png', TYPE_CONTROL)
            PLAYER_LIST.append(player)
            player_count += 1

            if player_count == number_of_player:
                stage += 1

                pygame.mixer.music.play(-1)

                print(PLAYER_LIST)
            else:
                TYPE_CONTROL = -1


def scene_pause():
    global running
    global pause

    # Все возможные отрисовки
    if buffs_in_game:
        for entity in buffs_in_game:
            entity.draw(screen)

    if boss_bullets_in_game:
        for entity in boss_bullets_in_game:
            entity.draw(screen)

    for pl in PLAYER_LIST:
        if pl.bullets_in_game:
            for entity in pl.bullets_in_game:
                entity.draw(screen)
        pl.draw(screen)

    if enemy_in_game:
        for entity in enemy_in_game:
            entity.draw(screen)
    if BOSS_IN_GAME:
        boss.draw(screen, boss_health)

    pygame.mixer.music.pause()

    alpha = pygame.Surface((WIDTH - 50, HEIGHT - 50))
    alpha.set_alpha(64)
    alpha.fill((255, 255, 255))
    alpha_rect = alpha.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(alpha, alpha_rect)

    if is_sound_on:
        btn_volume = Button('img/sound_on.png', 'img/sound_on.png', '', 0, 0, (50, 50))
    else:
        btn_volume = Button('img/sound_off.png', 'img/sound_off.png', '', 0, 0, (50, 50))

    btn_volume.draw(screen)

    text_pause = info_text.render('Пауза', True, 'White')
    text_pause_rect = text_pause.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    screen.blit(text_pause, text_pause_rect)

    btn_continue = Button('img/button1.png', 'img/button2.png', 'Продолжить', WIDTH // 2 - 100, HEIGHT // 2 + 25,
                          (200, 75))
    btn_exit = Button('img/button1.png', 'img/button2.png', 'Выход', WIDTH // 2 - 100, HEIGHT // 2 + 100,
                      (200, 75))

    btn_continue.update(screen)
    btn_exit.update(screen)
    btn_continue.draw(screen)
    btn_exit.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if btn_continue.is_click(event) or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
            pygame.mixer.music.unpause()
            pause = False
        elif btn_exit.is_click(event):
            running = False
        elif btn_volume.is_click(event):
            if is_sound_on:
                toggle_sound()
            else:
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
    else:
        is_sound_on = True

# -----------------------------


# Настройка игры
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(NAME_GAME)

# Настройка часов
clock = pygame.time.Clock()
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, random.randint(ENEMY_APPEAR_SPEED[0], ENEMY_APPEAR_SPEED[1]))
start_ticks = None


# Настройка музыки
sound_shoot = pygame.mixer.Sound('music/sound_shoot.mp3')
sound_shoot.set_volume(0.5)
sound_death_enemy = pygame.mixer.Sound('music/sound_death.mp3')
sound_death_enemy.set_volume(0.5)
pygame.mixer.music.load('music/background.mp3')
pygame.mixer.music.set_volume(0.2)
is_sound_on = True

# Настройка текста
info_text = pygame.font.Font('fonts/DelaGothicOne-Regular.ttf', 24)

# Вспомогательные переменные, которые возможно нужны
kind_buff = 0
record = None
boss_health = BOSS_HEALTH
pause = False

# Счетчик сцен (0 - Главное меню; 1 - Выбор количества игроков; 2 - Выбор управления; 3 - Игровое поле; 4 - Проигрыш)
stage = 0


# Основной цикл игры
running = True
while running:

    clock.tick(FPS)

    screen.fill('Black')

    # Главное меню
    if stage == 0:
        scene_main_menu()

    # Выбор количества игроков
    elif stage == 1:
        scene_sel_number_of_player()

    # Выбор управления
    elif stage == 2:
        scene_sel_ctrl_type()

    # Игровое поле
    if stage == 3:
        if is_game():
            # Музыка / не музыка
            if not is_sound_on:
                pygame.mixer.music.pause()

            # Ивенты
            for event in pygame.event.get():

                # Закрытие игры
                if event.type == pygame.QUIT:
                    running = False

                # Пауза
                if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                    pause = True
                    break

                # Пауза когда экран не в фокусе
                if event.type == pygame.ACTIVEEVENT:
                    if event.state == 2:
                        pause = True
                        break

                # Спавн врагов (Засунуть в класс?)
                if not BOSS_IN_GAME and event.type == enemy_timer and len(enemy_in_game) < ENEMY_COUNT_DIFFICULTY:

                    kind_enemy = random.randint(0, 1)
                    enemy = Enemy(kind_enemy)
                    enemy_in_game.append(enemy)

                    # Спавн врагов в зависимости от максимального количества очков
                    max_score = 0
                    for pl in PLAYER_LIST:
                        if pl.score >= max_score:
                            max_score = pl.score
                    if ENEMY_APPEAR_SPEED[0] - 20 * max_score <= 0:
                        BOSS_IN_GAME = True
                        boss = BossEvent('img/button1.png')
                    else:
                        pygame.time.set_timer(enemy_timer, random.randint(ENEMY_APPEAR_SPEED[0]-20*max_score,
                                                                          ENEMY_APPEAR_SPEED[1]-30*max_score))
                # Стрельба игрока
                for entity in PLAYER_LIST:
                    entity.shoot()

                # Атаки босса
                if BOSS_IN_GAME:
                    boss.shoot()
                    boss.fire()

            # Пауза
            if pause:
                scene_pause()

            # Не пауза
            else:
                # Отрисовка и столкновения баффов (в класс?)
                if buffs_in_game:
                    for entity in list(buffs_in_game):
                        entity.move()

                        if entity.y > HEIGHT:
                            buffs_in_game.remove(entity)

                        for pl in PLAYER_LIST:
                            if pl.rect.colliderect(entity.rect):
                                try:
                                    buffs_in_game.remove(entity)
                                    if entity.kind == 1:
                                        pl.lives += 1
                                    elif entity.kind == 2:
                                        pl.bullet += 1
                                    elif entity.kind == 3:
                                        pl.time = pygame.time.get_ticks()
                                        pl.infinite_bullet = True
                                except ValueError:
                                    print('Не удалось удалить бафф из списка')
                                    buff_player = random.randint(1, 2)
                                    if buff_player == 2 and PLAYER_LIST[1].lives > 0:
                                        if entity.kind == 1:
                                            PLAYER_LIST[1].lives += 1
                                            PLAYER_LIST[0].lives -= 1
                                        elif entity.kind == 2:
                                            PLAYER_LIST[1].bullet += 1
                                            PLAYER_LIST[0].bullet -= 1
                                        elif entity.kind == 3:
                                            start_ticks = pygame.time.get_ticks()
                                            PLAYER_LIST[1].time = pygame.time.get_ticks()
                                            PLAYER_LIST[0].time = 0
                                            PLAYER_LIST[1].infinite_bullet = True
                                            PLAYER_LIST[0].infinite_bullet = False

                # Отрисовка пуль босса
                if boss_bullets_in_game:
                    for entity in list(boss_bullets_in_game):
                        entity.move()
                        if entity.y > HEIGHT - entity.size[1]:
                            boss_bullets_in_game.remove(entity)

                        for pl in PLAYER_LIST:
                            if entity.rect.colliderect(pl.rect):
                                try:
                                    boss_bullets_in_game.remove(entity)
                                    pl.lives -= 1
                                except ValueError:
                                    pl.lives -= 1


                # Отрисовка игрока
                for pl in PLAYER_LIST:
                    if pl.bullets_in_game:
                        for entity in list(pl.bullets_in_game):
                            entity.move()
                            if entity.y < 0:
                                pl.bullets_in_game.remove(entity)
                    pl.move()
                    pl.draw(screen)

                # Отрисовка и столкновения врагов
                if enemy_in_game:
                    for entity in list(enemy_in_game):
                        entity.move()
                        if entity.y > HEIGHT or not (0 - entity.size[0] < entity.x < WIDTH):
                            enemy_in_game.remove(entity)
                        for pl in PLAYER_LIST:
                            if pl.rect.colliderect(entity.rect):
                                try:
                                    enemy_in_game.remove(entity)
                                    pl.lives -= 1
                                except ValueError:
                                    pl.lives -= 1
                                    print('Не удалось удалить врага из списка')

                            if pl.bullets_in_game:
                                for bullet in list(pl.bullets_in_game):
                                    if bullet.rect.colliderect(entity.rect):
                                        if entity in enemy_in_game:
                                            enemy_in_game.remove(entity)
                                            pl.bullets_in_game.remove(bullet)
                                            PLAYER_LIST[random.randint(0, len(PLAYER_LIST)-1)].score += 1
                                            sound_death_enemy.play()
                                        else:
                                            pl.bullets_in_game.remove(bullet)

                                        # Спавн Баффов
                                        if not pl.infinite_bullet:
                                            chance_buff = random.random()
                                            if len(buffs_in_game) < BUFF_AMOUNT:
                                                if chance_buff > BUFF_CHANCE_3:
                                                    kind_buff = 3
                                                elif chance_buff > BUFF_CHANCE_1:
                                                    kind_buff = 1
                                                elif chance_buff > BUFF_CHANCE_2:
                                                    kind_buff = 2

                                                if kind_buff != 0:
                                                    buff = FallingBuff(kind_buff)
                                                    buffs_in_game.append(buff)
                                                    kind_buff = 0

                if BOSS_IN_GAME:
                    boss.draw(screen, boss_health)
                    for pl in PLAYER_LIST:
                        if pl.bullets_in_game:
                            for entity in list(pl.bullets_in_game):
                                if entity.rect.colliderect(boss.rect):
                                    pl.bullets_in_game.remove(entity)
                                    boss_health -= 5

                    if boss_health <= 0:
                        for pl in PLAYER_LIST:
                            pl.lives = 0

                # Надписи на экране
                temp = 0
                for pl in PLAYER_LIST:
                    if pl.lives > 0:
                        info_life = info_text.render('Жизни: ' + str(pl.lives), True, 'White')
                        info_score = info_text.render('Очки: ' + str(pl.score), True, 'White')
                        if pl.infinite_bullet:
                            info_bullet = info_text.render('Пули: ∞', True, 'White')
                            seconds = (pygame.time.get_ticks()-pl.time)/1000
                            info_timer_infinity = info_text.render('00:0' + str(round(10-seconds)-1), True, 'Red')
                            screen.blit(info_timer_infinity, (temp, 70))
                            if seconds >= 9:
                                pl.infinite_bullet = False
                        else:
                            if pl.bullet - len(pl.bullets_in_game) <= 0:
                                info_bullet = info_text.render('Пули: 0', True, 'White')
                            else:
                                info_bullet = info_text.render('Пули: ' + str(pl.bullet - len(pl.bullets_in_game)), True, 'White')
                    else:
                        info_life = info_text.render('Жизни: 0', True, 'White')
                        info_score = info_text.render('Очки: ' + str(pl.score), True, 'White')
                        info_bullet = info_text.render('Пули: 0', True, 'White')

                    screen.blit(info_life, (temp, 0))
                    screen.blit(info_score, (temp, 24))
                    screen.blit(info_bullet, (temp, 48))
                    temp += WIDTH - 200

        # Переключение сцены
        else:
            stage += 1

    # Экран проигрыша/выигрыша
    elif stage == 4:

        pygame.mixer.music.stop()

        if not record:
            file_record = open('high_record.txt', 'r')
            try:
                record = int(file_record.readline())
            except ValueError:
                print('Ошибка! В файле не число!')
            file_record.close()

        else:
            max_score = 0
            winner = -1
            for (el, pl) in enumerate(PLAYER_LIST):
                if pl.score > max_score:
                    max_score = pl.score
                    if winner == el:
                        winner = 3
                        break
                    winner = el
            if max_score >= record:
                file_record = open('high_record.txt', 'w')
                record = max_score
                file_record.write(str(record))
                file_record.close()

            if number_of_player == 2:
                if winner != -1:
                    text_winner = info_text.render('Победитель: Игрок ' + str(winner+1), True, 'White')
                    text_winner_rect = text_winner.get_rect(center=(WIDTH//2, HEIGHT//2 - 100))
                    screen.blit(text_winner, text_winner_rect)
                else:
                    text_winner = info_text.render('Победила Дружба!', True, 'White')
                    text_winner_rect = text_winner.get_rect(center=(WIDTH//2, HEIGHT//2 - 100))
                    screen.blit(text_winner, text_winner_rect)

        text_record = info_text.render('Рекорд: ' + str(record), True, 'White')
        screen.blit(text_record, (0, 24))

        text_death = info_text.render('Потрачено', True, 'White')
        text_death_rect = text_death.get_rect(center=(WIDTH//2, HEIGHT//2))

        screen.blit(text_death, text_death_rect)

        btn_retry = Button('img/button1.png', 'img/button2.png', 'Заново', WIDTH//2-70, HEIGHT//2+25, (140, 75))
        btn_retry.update(screen)

        btn_exit = Button('img/button1.png', 'img/button2.png', 'Выход', WIDTH//2-70, HEIGHT//2+90, (140, 75))
        btn_exit.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if btn_retry.is_click(event):
                stage = 3
                record = None
                BOSS_IN_GAME = False
                boss_health = BOSS_HEALTH
                enemy_in_game.clear()
                boss_bullets_in_game.clear()
                buffs_in_game.clear()
                pygame.mixer.music.play(-1)
                print(PLAYER_LIST)
                for pl in PLAYER_LIST:
                    pl.infinite_bullet = False
                    pl.lives = LIVES
                    pl.bullet = AMOUNT_BULLET
                    pl.bullets_in_game.clear()
                    pl.score = 0

            elif btn_exit.is_click(event):
                running = False

    # Вывод в консоль контрольных значений
    # print('-------------------')
    # print('Координаты игрока: ', player.x, player.y)
    # print('Координаты ректа игрока: ', player.rect.x, player.rect.y)
    # print('Количество врагов на экране: ', len(enemy_in_game))
    # print('Количетсво пуль на экране: ', len(boss_bullets_in_game))
    # print('Рект у игрока:', player.rect)
    # print('Жив? ', current_lives, SCORE)
    # print('-------------------\n')

    pygame.display.update()

pygame.quit()
