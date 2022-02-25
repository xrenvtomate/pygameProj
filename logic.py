import pygame as pg
import random
from math import sin, cos, atan, pi
from other import *

def direction(x1, x2):
    if x1 > x2:
        return 1
    elif x1 < x2:
        return -1
    return 0


def spawnkd(score): #
    if score < 50:
        return 1800
    if score < 100:
        return 1400
    if score < 200:
        return 1000
    if score < 400:
        return 700
    if score < 1000:
        return 400
    return 300


def drawinterface(sc, player):
    # weapon bar
    for i, weapon in enumerate(player.weapons):
        pg.draw.rect(sc, (0, 100, 0), (i * 100, 0, 100, 100), 0, 10)
        sc.blit(pg.transform.scale(img[weapon], (100, 100)), (i * 100, 0))
        pg.draw.rect(sc, (100, 255, 100), (i * 100, 0, 100, 100), 8, 10)

    # player hp
    pg.draw.rect(sc, (255 * (1 - player.hp / maxhp), 255 * player.hp / maxhp, 0),
                 (10, 100, 200 * player.hp / maxhp, 60), 0, 30)
    pg.draw.rect(sc, (0, 0, 0), (10, 100, 200, 60), 6, 30)


def drawmap():
    sc = pg.surface.Surface((map_w * tile, map_h * tile), pg.SRCALPHA)
    for y in range(map_h - 1, -1, -1):
        for x in range(map_w):
            kordx, kordy = x * tile, height - (map_h - y) * tile
            if map[y][x] == '#':
                sc.blit(img['gnd'], (kordx, kordy))
                Border(kordx, kordy, kordx + tile, kordy, 'up')
            elif map[y][x] == 'H':
                sc.blit(img['earth' + str(random.randint(1, 2))], (kordx, kordy))
                Border(kordx, kordy, kordx + tile, kordy, 'up')
            elif map[y][x] == '_':
                sc.blit(img['platf'], (kordx, kordy))
                Border(kordx, kordy, kordx + tile, kordy, 'up')
                Border(kordx, kordy + platf_w, kordx + tile, kordy + platf_w, 'down')
                if map[y][x - 1] != '_' and x > 0:
                    Border(kordx, kordy, kordx, kordy + platf_w, 'vert')
                if map[y][x + 1] != '_' and x < len(map[0]) - 1:
                    Border(kordx + tile, kordy, kordx + tile, kordy + platf_w, 'vert')
            elif map[y][x] == '@':
                ppos = kordx, kordy - 20


    return sc, ppos


class Player(pg.sprite.Sprite):
    def __init__(self, ppos):
        super().__init__(all_sprites)
        imgr = img['pers']
        imgr.set_colorkey(imgr.get_at((0, 0)))
        self.imgr = imgr
        self.imgl = pg.transform.flip(imgr, True, False)
        self.imgl.set_colorkey(imgr.get_at((0, 0)))
        self.image = imgr
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = ppos
        self.vx = self.vy = 0
        self.on_grnd = False
        self.morgens = 0
        self.hp = maxhp
        self.chosen_weapon = None
        self.weapons = []
        self.diss = 0
        self.v_bul = v_bul
        self.v_dis = v_dis

    def moving(self):
        if pg.sprite.spritecollideany(self, vert_bord) and not self.on_grnd:
            self.rect.x -= self.vx
            self.vx = 0

        if pg.sprite.spritecollideany(self, up_bord):
            self.on_grnd = True
            self.vy = 0
        else:
            self.on_grnd = False
            self.vy += g

        if pg.sprite.spritecollideany(self, down_bord):
            self.rect.y -= min(self.vy, -1)
            self.vy = 0


        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.image = self.imgl
            if abs(self.vx) <= self.max_v:
                self.vx -= 1
        elif self.vx < 0:
            self.vx += 1
        if keys[pg.K_d]:
            self.image = self.imgr
            if abs(self.vx) <= self.max_v:
                self.vx += 1
        elif self.vx > 0:
            self.vx -= 1
        if keys[pg.K_SPACE] and self.on_grnd:
            self.on_grnd = False
            self.vy = -jump_pwr


        if not self.on_grnd:
            self.rect.y += self.vy

        self.rect.x += self.vx

    def update(self):
        self.moving()
        self.rect.centerx = max(min(world_w, self.rect.centerx), 0)
        self.max_v = max_v * min(2, 1 + self.morgens / 5)
        self.v_bul = v_bul * min(2, 1 + self.morgens / 5)
        self.v_dis = v_dis * min(2, 1 + self.morgens / 5)
        for item in pg.sprite.spritecollide(self, items, True):
            if item.type == 'weapon':
                if item.name not in self.weapons:
                    self.weapons.append(item.name)
            elif item.type == 'heal':
                self.hp = min(maxhp, self.hp + 1)
            else:
                self.hp = maxhp
                self.morgens += 1

        keys = pg.key.get_pressed()
        if keys[pg.K_1]:
            self.chosen_weapon = None
        elif keys[pg.K_2]:
            try:
                self.chosen_weapon = self.weapons[0]
            except:
                self.chosen_weapon = None
        elif keys[pg.K_3]:
            try:
                self.chosen_weapon = self.weapons[1]
            except:
                self.chosen_weapon = None

    def shooting(self, pos):
        ang = atan((pos[1] - self.rect.y - self.rect.h // 2) / (pos[0] - self.rect.x - self.rect.w // 2 + 0.5))
        if pos[0] < self.rect.x + self.rect.w // 2:
            ang += pi
        if self.chosen_weapon == 'pistol':
            Bullet(self.v_bul, ang, (self.rect.x + self.rect.w // 2, self.rect.y + self.rect.h // 2), img['pist_bullet'])
        elif self.chosen_weapon == 'dis':
            Bullet(self.v_dis * (1 + self.morgens / 3), ang, (self.rect.x + self.rect.w // 2, self.rect.y + self.rect.h // 2), img['dis'])
            Bullet(self.v_dis * (1 + self.morgens / 3), ang - pi / 40, (self.rect.x + self.rect.w // 2, self.rect.y + self.rect.h // 2), img['dis'])
            Bullet(self.v_dis * (1 + self.morgens / 3), ang + pi / 40, (self.rect.x + self.rect.w // 2, self.rect.y + self.rect.h // 2), img['dis'])


class Border(pg.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2, type):
        super().__init__()

        if type == 'vert':  # вертикальная стенка
            self.add(vert_bord)
            self.rect = pg.Rect(x1, y1, 1, y2 - y1)
        elif type == 'up':  # горизонтальная стенка
            self.add(up_bord)
            self.rect = pg.Rect(x1, y1, x2 - x1, 1)
        else:
            self.add(down_bord)
            self.rect = pg.Rect(x1, y1, x2 - x1, 1)


class Item(pg.sprite.Sprite):
    def __init__(self, name, type, pos):
        super().__init__(all_sprites, items)
        self.type = type
        self.image = img[name]
        self.name = name
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.vy = 0
        self.on_gnd = False

    def update(self):

        if not pg.sprite.spritecollideany(self, up_bord):
            if not self.on_gnd:
                self.vy += g / 2
                self.rect.y += self.vy
            else:
                self.on_gnd = True
                self.rect.y -= self.vy


class Bullet(pg.sprite.Sprite):
    def __init__(self, v, ang, pos, img):
        super().__init__(all_sprites, bullets)
        self.image = img
        self.dx = v * cos(ang)
        self.dy = v * sin(ang)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos

    def update(self):
        if (not -200 < self.rect.x < world_w + 200) or (not -200 < self.rect.y < height + 200):
                self.kill()
        self.rect.x += self.dx
        self.rect.y += self.dy


class Anim_sprite(pg.sprite.Sprite):
    def __init__(self, img_name, num_frames, size):
        super().__init__(all_sprites, anim_sprites)
        self.frames = []
        self.cur_fr = 0
        self.num_fr = num_frames
        for i in range(num_frames):
            self.frames.append(load_img(f'{img_name}{i}.png', (size)))
        self.anim()

    def anim(self):
        self.image = self.frames[self.cur_fr]
        self.cur_fr = (self.cur_fr + 1) % self.num_fr


class Green_enemy(Anim_sprite):
    def __init__(self, pos, right):
        super().__init__('green_enem', 2, pers_size)
        self.add(enemies)
        self.hp = self.mhp = 3
        self.vx = 5 * right
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos

    def moving(self, ppos):
        self.rect = self.rect.move(self.vx, 0)

    def shoted(self, dmg):
        self.hp -= dmg
        if self.hp == 0:
            self.kill()
            rnd = random.random()
            if rnd > 0.8:
                Item('heal', 'heal', (self.rect.x + 10, self.rect.y + self.rect.h - 50))
            return 10
        return 0


class Flyer(Anim_sprite):
    def __init__(self, pos):
        super().__init__('fly', 3, pers_size)
        self.add(enemies)
        self.hp = self.mhp = 2
        self.v = 3
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos

    def moving(self, ppos):
        self.rect = self.rect.move(self.v * direction(ppos[0], self.rect.x + self.rect.w // 2),
                                   self.v * direction(ppos[1], self.rect.y + self.rect.h // 2))
    def shoted(self, dmg):
        self.hp -= dmg
        if self.hp == 0:
            rnd = random.random()
            if rnd > 0.9:
                Item('dis', 'weapon', (self.rect.x + 10, self.rect.y + self.rect.h - 50))
            elif rnd > 0.75:
                Item('heal', 'heal', (self.rect.x + 10, self.rect.y + self.rect.h - 50))
            self.kill()
            return 15
        return 0


class Obed(pg.sprite.Sprite):
    def __init__(self, vy, pos):
        super().__init__(enemies, all_sprites)
        self.vy = vy
        self.vx = 10 if pos[0] < 0 else -10
        self.image = img['obed']
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.hp = self.mhp = 1

    def moving(self, ppos):
        self.rect = self.rect.move(self.vx, self.vy)
        self.vy += g / 3

    def shoted(self, dmg):
        rnd = random.random()
        if rnd > 0.9:
            Item('heal', 'heal', (self.rect.x + 10, self.rect.y + self.rect.h - 50))
        elif rnd > 0.82:
            Item('morgen', 'bonus', (self.rect.x + 10, self.rect.y + self.rect.h - 50))
        self.kill()
        return 5 


class Uutn(Obed):
    def __init__(self, vx, posx):
        super().__init__(0, (0, 0))
        self.vy = 0
        self.vx = vx
        self.image = img['uutn']
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = posx, -100
        self.hp = self.mhp = 1


class CameraGroup(pg.sprite.Group):
    def __init__(self):
        super().__init__()

    def get_offset(self, target, pos0):
        self.dy = 0
        self.dx = max(target.rect.centerx - width // 2, 0)# + width // 2)
        self.dx = min(self.dx, world_w - width)

    def draw_sprites(self, player, sc, pos0, fon):
        self.get_offset(player, pos0)
        sc.blit(fon, (-self.dx, self.dy))

        # sprites
        for sprite in self.sprites():
            sc.blit(sprite.image, (sprite.rect.x - self.dx, sprite.rect.y - self.dy))

        # chosen weapon
        if player.chosen_weapon:
            sc.blit(img[player.chosen_weapon], (player.rect.x + 10 - self.dx , player.rect.y - 40))

all_sprites = CameraGroup()