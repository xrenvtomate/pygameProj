import pygame as pg
import os
#from logic import *


def load_img(img, size):
    img = pg.image.load(os.path.join('data', img)).convert_alpha()
    return pg.transform.scale(img, size)

pg.init()

up_bord = pg.sprite.Group()
down_bord = pg.sprite.Group()
vert_bord = pg.sprite.Group()
items = pg.sprite.Group()
bullets = pg.sprite.Group()
anim_sprites = pg.sprite.Group()
enemies = pg.sprite.Group()

# constants
width, height = 1280, 720
tile = 40
pers_size = 40, 60
g = 0.5
max_v = 7
v_bul = 15
v_dis = 10
jump_pwr = 12
maxhp = 5

sc = pg.display.set_mode((width, height))

img = {  # images dict

    'gnd': load_img('ground.png', (tile, tile)),
    'platf': load_img('platf.png', (tile, tile)),
    'bg': load_img('background.jpg', (width, height)),
    'earth1': load_img('earth1.png', (tile, tile)),
    'earth2': load_img('earth2.png', (tile, tile)),
    'pistol': load_img('pistol.png', (40, 40)),
    'pers': load_img('pers.png', pers_size),
    'pist_bullet': load_img('pist_bullet.png', (10, 10)),
    'heal': load_img('heal.png', (30, 30)),
    'dis': load_img('dis.png', (40, 40)),
    'startscreen': load_img('startscreen.jpg', (width, height)),
    'gameover': load_img('gameover.jpg', (width, height)),
    'obed': load_img('obed.png', (100, 80)),
    'uutn': load_img('uutn.png', (100, 80)),
    'morgen': load_img('morgen.png', (100, 80))
}
platf_w = tile // 2

with open('data\map.txt') as maptxt:  # map reading
    map = [i.rstrip() for i in maptxt.readlines()]
map_w, map_h = len(map[0]), len(map)
world_w, world_h = map_w * tile, map_h * tile