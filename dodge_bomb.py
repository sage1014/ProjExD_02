import sys
import pygame as pg
import random

WIDTH, HEIGHT = 1600, 900


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    """爆弾"""
    enn = pg.Surface((20, 20))
    pg.draw.circle(enn, (255, 0, 0), (10, 10), 10)
    enn.set_colorkey((0, 0, 0))
    bom_rect = enn.get_rect() # SurfaceからRectを抽出
    x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    bom_rect.center = (x, y)
    """こうかとん"""
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = (x, y)
    clock = pg.time.Clock()

    tmr = 0
    while True:
        delta = {
        pg.K_UP:    (0, -5),
        pg.K_DOWN:  (0, +5),
        pg.K_LEFT:  (-5, 0),
        pg.K_RIGHT: (+5, 0),
        }
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        for key, mv in delta.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]

        screen.blit(bg_img, [0, 0])
        #screen.blit(kk_img, [900, 400])

        """こうかとん"""
        kk_rct.move_ip(sum_mv[0], sum_mv[1])
        screen.blit(kk_img, kk_rct)

        """爆弾"""
        bom_rect.move_ip(5, 5)
        screen.blit(enn, bom_rect)

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()