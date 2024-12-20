# Импорт библиотек
import pygame
import random
from sys import exit

# Инициализация pygame
pygame.init()
pygame.time.set_timer(pygame.USEREVENT, 1000)

# Создание игрового поля
screen = pygame.display.set_mode((1200, 675))
pygame.display.set_caption('Argonaute Defense')
icon = pygame.image.load('risc.ico')
pygame.display.set_icon(icon)

# Загрузка изображений
clock = pygame.time.Clock()
cell = pygame.image.load('cell.png').convert()
nucleus = pygame.image.load('nucleus.png').convert_alpha()

# Создание надписей
font = pygame.font.Font('pixelfont.ttf', 70)
sfont = pygame.font.Font('pixelfont.ttf', 30)
name = font.render('Argonaute Defense', False, 'Black')

# Класс игрока (белка RLC)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('rlc.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=(130, 580))
        self.speedx = 0

    def update(self):
        # Контроль игрока клавишами
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -10
        elif keystate[pygame.K_RIGHT]:
            self.speedx = 10
        else:
            self.speedx = 0
        # Контроль игрока мышкой или тачпадом
        pressed = pygame.mouse.get_pressed()
        if pressed[0] or pressed[2]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.rect.centerx = mouse_x

        # Обновление позиции игрока
        self.rect.x += self.speedx

        # Ограничение движения по экрану
        if self.rect.right > 1200:
            self.rect.right = 1200
        if self.rect.left < 0:
            self.rect.left = 0

# Классы летающих элементов, из которых нужно собирать комплекс
class Dicer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('dicer.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = random.randrange(0, 170)
        self.rect.x = random.randrange(1030, 1200)
        self.speedy = random.randint(1, 2)
        self.speedx = random.randint(3, 4)

    def update(self):
        if self.rect.y < 675 and self.rect.x > -100:
            self.rect.y += self.speedy
            self.rect.x -= self.speedx

class Trbp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('trbp.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = random.randrange(0, 170)
        self.rect.x = random.randrange(1030, 1200)
        self.speedx = random.randint(1, 2)
        self.speedy = random.randint(3, 4)

    def update(self):
        if self.rect.y < 675 and self.rect.x > -100:
            self.rect.y += self.speedy
            self.rect.x -= self.speedx

class Ago2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('ago2.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = random.randrange(0, 170)
        self.rect.x = random.randrange(1030, 1200)
        self.speedy = random.randint(1, 2)
        self.speedx = random.randint(3, 4)

    def update(self):
        if self.rect.y < 675 and self.rect.x > -100:
            self.rect.y += self.speedy
            self.rect.x -= self.speedx

class Rna(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('mirna.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = random.randrange(0, 170)
        self.rect.x = random.randrange(1030, 1200)
        self.speedx = random.randint(1, 2)
        self.speedy = random.randint(3, 4)

    def update(self):
        if self.rect.y < 675 and self.rect.x > -100:
            self.rect.y += self.speedy
            self.rect.x -= self.speedx

# Создание групп спрайтов
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

dicers = pygame.sprite.Group()
dicer = Dicer()
dicers.add(dicer)

trbps = pygame.sprite.Group()
trbp = Trbp()
trbps.add(trbp)

agos2 = pygame.sprite.Group()
ago2 = Ago2()
agos2.add(ago2)

# Контроль столкновений для сборки комплекса RISC
def handle_collisions(player, all_sprites):
    global score

    image_rd = pygame.image.load('rd.png').convert_alpha()
    image_rdt = pygame.image.load('rdt.png').convert_alpha()
    image_rdta = pygame.image.load('rdta.png').convert_alpha()
    image_fullrisc = pygame.image.load('fullrisc.png').convert_alpha()
    image_rlc = pygame.image.load('rlc.png').convert_alpha()

    for sprite in all_sprites:
        if pygame.sprite.collide_rect(player, sprite):
            if isinstance(sprite, Dicer):
                player.image = image_rd
            all_sprites.update()
            
    for sprite in all_sprites:
        if pygame.sprite.collide_rect(player, sprite):
            if isinstance(sprite, Trbp) and player.image == image_rd:
                player.image = image_rdt
            all_sprites.update()

     for sprite in all_sprites:
        if pygame.sprite.collide_rect(player, sprite):
            if isinstance(sprite, Ago2) and player.image == image_rdt:
                player.image = image_rdta
            all_sprites.update()
            
     for sprite in all_sprites:
         if pygame.sprite.collide_rect(player, sprite):
             if isinstance(sprite, Rna) and player.image == image_rdta:
                player.image = image_fullrisc
            all_sprites.update()
                score -= 50  # Уменьшаем счет на 50
                player.image = image_rlc  # Возвращаем к начальному изображению

# Экран заставки
def show_go_screen(score):
    screen.blit(cell, (0, 0))
    screen.blit(nucleus, (1030, 0))
    name_surf = font.render("Argonaute Defense", False, 'Black')
    nsr = name_surf.get_rect(center=(600,330))
    instruction = sfont.render("Нажмите пробел, чтобы начать", False, 'Black')
    instr_rect = instruction.get_rect(center=(600, 450))
    screen.blit(name_surf, nsr)
    screen.blit(instruction, instr_rect)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

# Создание физических объектов классов
player = Player()
dicer = Dicer()
trbp = Trbp()
ago2 = Ago2()
rna = Rna()

all_sprites = pygame.sprite.Group()
all_sprites.add(player, dicer, trbp, ago2, rna)

# Основной игровой цикл
score = 0
game_over = True
while True:
    if game_over:
        show_go_screen(score)
        game_over = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.USEREVENT:
            score += 1
            new_rna = Rna()
            new_ago2 = Ago2()
            new_trbp = Trbp()
            new_dicer = Dicer()
            all_sprites.add(new_rna,new_ago2,new_trbp,new_dicer)

    # Обновление состояния всех спрайтов
    all_sprites.update()

    # Обработка столкновений
    handle_collisions(player, all_sprites)

    # Рисовка объектов на экране
    screen.blit(cell, (0, 0))
    sfont = pygame.font.Font('pixelfont.ttf', 30)
    tscore = sfont.render("Вирусной РНК: " + str(score) + " копий", False, 'Black')
    all_sprites.draw(screen)
    screen.blit(nucleus, (1030, 0))
    screen.blit(name, (60, 45))
    screen.blit(tscore, (65,20))

    # Контроль обновления всего цикла и контроль FPS
    pygame.display.update()
    clock.tick(60)
