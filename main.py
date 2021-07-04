import pygame
from pygame.locals import *
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
fps = 60
game_over = False
win = False
font = pygame.font.SysFont(None, 24)
start = True
start_menu = font.render('Platformer made by Bakhtiyar Abdibek. Click to continue', True, (0, 0, 0))
game_over_text = font.render('You failed to get to the princess. Press any button to retry', True, (0, 0, 0))
win_text = font.render('You won!!!', True, (0, 0, 0))
print(game_over_text.get_width())
print(game_over_text.get_height())


class World():
    def __init__(self, data):
        self.tile_list = []


        dirtblock_img = pygame.image.load('dirtblock.png')
        dirtblock_img = pygame.transform.scale(dirtblock_img, (tile_size, tile_size))


        r_count = 0
        for row in data:
            c_count = 0
            for tile in row:
                if tile == 1:
                    img = dirtblock_img
                    img_rect = img.get_rect()
                    img_rect.x = c_count * tile_size
                    img_rect.y = r_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    enemy = Enemy(c_count * tile_size, r_count * tile_size)
                    enemy_group.add(enemy)
                if tile == 3:
                    slime = Slime_Enemy(c_count * tile_size, r_count * tile_size)
                    enemy_group.add(slime)
                c_count += 1
            r_count += 1
    def draw(self):
        for tile in self.tile_list:
            window.blit(*tile)


class Player():
    def __init__(self, x, y):
        img = pygame.image.load('m1.png')
        self.img = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.w = self.img.get_width()
        self.rect.y = y
        self.h = self.img.get_height()
        self.vel_y = 0
        self.jumped = False
    def update(self):
        global game_over
        global win
        dx = 0
        dy = 0

        if not (game_over or win):
        
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                dx -= 4
            if key[pygame.K_SPACE] and self.jumped == False:
                self.vel_y = -16
                self.jumped = True
            if key[pygame.K_RIGHT]:
                dx += 4

            self.vel_y += 1
            if self.vel_y > 5:
                self.vel_y = 5
            dy += self.vel_y

            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.w, self.h):
                    dx = 0

                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.w, self.h):
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.jumped = False

            if pygame.sprite.spritecollide(self, enemy_group, False):
                game_over = True

            self.rect.x += dx
            self.rect.y += dy

        window.blit(self.img, self.rect)
        return game_over


class Goal():
    def __init__(self, x, y):
        img = pygame.image.load('princess.png')
        self.img = pygame.transform.scale(img, (30, 60))
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
    def draw(self):
        window.blit(self.img, self.rect)


class Enemy(pygame.sprite.Sprite):
    def  __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('enemy.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.w = self.image.get_width()
        self.rect.y = y
        self.h = self.image.get_height()
        self.move = 1
        self.vel_y = 0
    def update(self):
        dx = 0
        dy = 0

        if self.rect.x > player.rect.x and distance(self.rect.x, self.rect.y, player.rect.x, player.rect.y) < 240:
            dx -= self.move
        if self.rect.x < player.rect.x and distance(self.rect.x, self.rect.y, player.rect.x, player.rect.y) < 240:
            dx += self.move

        self.vel_y += 1
        if self.vel_y > 5:
            self.vel_y = 5
        dy += self.vel_y

        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.w, self.h):
                dx = 0

            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.w, self.h):
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.jumped = False

        self.rect.x += dx
        self.rect.y += dy


class Slime_Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('slimeenemy.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.w = self.image.get_width()
        self.rect.y = y
        self.h = self.image.get_height()
        self.move = 1
        self.vel_y = 0
        self.jumped = False
    def update(self):
        dx = 0
        dy = 0

        if self.rect.x > player.rect.x and distance(self.rect.x, self.rect.y, player.rect.x, player.rect.y) < 240:
            dx -= self.move
        if self.rect.x < player.rect.x and distance(self.rect.x, self.rect.y, player.rect.x, player.rect.y) < 240:
            dx += self.move
        if distance(self.rect.x, self.rect.y, player.rect.x, player.rect.y) < 120 and self.jumped == False:
            self.vel_y = -16
            self.jumped = True

        self.vel_y += 1
        if self.vel_y > 5:
            self.vel_y = 5
        dy += self.vel_y

        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.w, self.h):
                dx = 0

            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.w, self.h):
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.jumped = False

        self.rect.x += dx
        self.rect.y += dy
def distance(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


window_size = (960, 420)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption('Platformer')

tile_size = 30

background_img = pygame.image.load('background1.png') 
background_img = pygame.transform.scale(background_img, (window_size))


block_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
enemy_group = pygame.sprite.Group()
world = World(block_data)
player = Player(tile_size*1, tile_size*12)
princess = Goal(tile_size* 30, tile_size * 11)


running = True
while running:
    clock.tick(fps)
    window.blit(background_img, (0, 0))
    if start:
        window.blit(start_menu, (0, 0))
    else:
        world.draw()

        if not (game_over or win):
            enemy_group.update()
        elif game_over:
            window.blit(game_over_text, ((window_size[0] - game_over_text.get_width()) / 2, (window_size[1] - game_over_text.get_height()) / 2))
        elif win:
            window.blit(win_text, ((window_size[0] - win_text.get_width()) / 2, (window_size[1] - win_text.get_height()) / 2))
        enemy_group.draw(window)
    
        game_over = player.update()
        princess.draw()
        if player.rect.colliderect(princess.rect):
            win = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and game_over:
            enemy_group = pygame.sprite.Group()
            world = World(block_data)
            player = Player(tile_size*1, tile_size*12)
            game_over = False
        if event.type == pygame.MOUSEBUTTONDOWN and start:
            start = False
    pygame.display.update()
pygame.quit()