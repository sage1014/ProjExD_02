import sys
import pygame as pg
import random

WIDTH, HEIGHT = 1600, 900

def check_screen(obj_rct: pg.Rect):
    """
    引数：こうかとんRectかばくだんRect
    戻り値；タプル　（横方方向判定結果, 縦方向判定結果)
    画面内ならTrue, 画面外ならFalse
    """
    width, height = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        width = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        height = False

    return width, height


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    #screen = pg.display.set_mode((1680, 15))

    """爆弾"""
    bom_img = pg.Surface((20, 20))
    pg.draw.circle(bom_img, (255, 0, 0), (10, 10), 10)
    bom_img.set_colorkey((0, 0, 0))
    bom_rect = bom_img.get_rect() # SurfaceからRectを抽出
    x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    bom_rect.center = (x, y)
    vx, vy = +5, +5

    """こうかとん"""
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = (900, 400)
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

        """こうかとん"""
        kk_rct.move_ip(sum_mv[0], sum_mv[1])
        if check_screen(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)

        """爆弾"""
        bom_rect.move_ip(vx, vy)
        width, height = check_screen(bom_rect)
        if not width:
            vx *= -1
        if not height:
            vy *= -1
        screen.blit(bom_img, bom_rect)

        """ゲームオーバー"""
        if kk_rct.colliderect(bom_rect):
            print("ゲームオーバー")
            return

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()