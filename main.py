from other import *
from logic import *
import random



if __name__ == '__main__':

    font = pg.font.Font(None, 100) # font settings
    mfont = pg.font.Font(None, 30)
    startfont = pg.font.Font(None, 60)
    clock = pg.time.Clock()
    a = 55
    # start screen
    sc.blit(img['startscreen'], (0, 0))
    with open('data\startscreentext.txt', encoding='utf-8') as txt:
        lns = txt.readlines()
        for i in range(len(lns)):
            sc.blit(startfont.render(lns[i].strip(), 1, '#18CEFF'), (50, 60 + i * 60))
    pg.display.flip()

    in_start_screen = True
    while in_start_screen:
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                exit()
            elif ev.type == pg.MOUSEBUTTONDOWN:
                in_start_screen = False


    # setup
    
    fon, startpos = drawmap()
    player = Player(startpos)
    score = 0

    Item('pistol', 'weapon', (random.randrange(world_w - tile), 0))
    running = True
    unkill = False
    unkillev = pg.USEREVENT + 3
    canshot = True
    kdev = pg.USEREVENT + 4

    spawnev = pg.USEREVENT + 1
    animev = pg.USEREVENT + 2
    pg.time.set_timer(animev, 100)
    pg.time.set_timer(spawnev, 10)

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
            elif event.type == pg.MOUSEBUTTONDOWN and canshot:  # shooting
                player.shooting((event.pos[0] + all_sprites.dx, event.pos[1]))
                canshot = False
                pg.time.set_timer(kdev, 200)

            elif event.type == spawnev: # mobs spawn
                rnd = random.random()
                if rnd > 0.8:
                    right = random.randint(0, 1)
                    Green_enemy((0 if right else world_w, height - 2 * tile - pers_size[0]), right * 2 - 1)
                elif rnd > 0.6:
                    Flyer((random.randrange(world_w), -20))
                elif rnd > 0.3:
                    Obed(random.randrange(0, -10, -1), (-100 + random.randint(0, 1) * (world_w + 100), random.randrange(world_h)))
                else:
                    Uutn(random.randint(-10, 10), random.randrange(world_w))
                kd = spawnkd(score)
                pg.time.set_timer(spawnev, random.randrange(kd, int(kd * 1.3)))


            # animing sprites
            elif event.type == animev:
                pg.time.set_timer(animev, 100)
                for sprt in anim_sprites:
                    sprt.anim()

            elif event.type == unkillev:
                unkill = False

            elif event.type == kdev:
                canshot = True



        sc.blit(img['bg'], (0, 0))

        for enem in enemies: # moving of enemies
            if (not -200 < enem.rect.x < world_w + 200) or (not -200 < enem.rect.y < world_h + 200):
                enem.kill()
            enem.moving((player.rect.x + player.rect.w // 2, player.rect.y + player.rect.h // 2))
            pg.draw.rect(sc, (255 * (1 - enem.hp / enem.mhp), 255 * enem.hp / enem.mhp, 100), (enem.rect.x - all_sprites.dx, enem.rect.y - 20, 40 * enem.hp / enem.mhp, 10), 0, 5)
            pg.draw.rect(sc, (50, 50, 50), (enem.rect.x - all_sprites.dx, enem.rect.y - 20, 40, 10), 2, 5)


        for bul, enems in pg.sprite.groupcollide(bullets, enemies, True, False).items():
            for enem in enems: # collision between bullets and wnemies
                score += enem.shoted(1)

        if pg.sprite.spritecollideany(player, enemies) and not unkill: # damage from enemies
            player.hp -= 1
            if player.hp == 0:
                running = False
            unkill = True
            pg.time.set_timer(unkillev, 400)


        all_sprites.update()
        
        # drawing objects

        all_sprites.draw_sprites(player, sc, startpos, fon)
        drawinterface(sc, player)
        # score 
        sc.blit(font.render(str(score), 1, '#FF1853'), (50, 300))
        # morgens
        sc.blit(mfont.render('?????????????? ??????????????????????????: ' + str(player.morgens), 1, '#FFE918'), (50, 400))
        pg.display.flip()
        clock.tick(60)

    # gameover screen
    endscreen = img['gameover']
    endscreen.blit(font.render(str(score), 1, '#8DFF18'), (world_w // 2, world_h // 2))
    for i in range(121): # 2 second animation
        sc.blit(endscreen, (-world_w + world_w * i / 120, 0))
        pg.display.flip()
        clock.tick(60)
    while True:
        for ev in pg.event.get():
            if ev.type in (pg.QUIT, pg.MOUSEBUTTONDOWN):
                exit()
