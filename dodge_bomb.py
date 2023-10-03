import sys
import pygame as pg
import random
import time

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
    screen = pg.display.set_mode((WIDTH, HEIGHT))   #　スクリーンの設定
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")    # 背景
    font = pg.font.Font(None, 80)   # Game Over用のFont
    mode = True # ゲームオーバーしているか

    """爆弾"""
    bom_img = pg.Surface((20, 20))  # 爆弾の作成
    pg.draw.circle(bom_img, (255, 0, 0), (10, 10), 10)
    bom_img.set_colorkey((0, 0, 0)) # 余計な部分を透明
    bom_rect = bom_img.get_rect() # SurfaceからRectを抽出
    x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT)  # 座標をランダム化
    bom_rect.center = (x, y)
    vx, vy = +5, +5 # 移動量

    """こうかとん"""
    kk_img = pg.image.load("ex02/fig/3.png")    # こうかとんの読み込み
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = (900, 400)
    dmg_kk = pg.image.load("ex02/fig/8.png")    # ゲームオーバー用のこうかとん
    dmg_kk = pg.transform.rotozoom(dmg_kk, 0, 2.0)


    clock = pg.time.Clock()

    tmr = 0 # タイマー
    while True:
        if mode:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return

            """矢印キー判定(移動量)"""
            delta = {   # 矢印キーと移動量の辞書
            pg.K_UP:    (0, -5),
            pg.K_DOWN:  (0, +5),
            pg.K_LEFT:  (-5, 0),
            pg.K_RIGHT: (+5, 0),
            }
            key_lst = pg.key.get_pressed()
            sum_mv = [0, 0]
            for key, mv in delta.items():
                if key_lst[key]:
                    sum_mv[0] += mv[0]
                    sum_mv[1] += mv[1]

            screen.blit(bg_img, [0, 0])

            """こうかとん"""    # こうかとんが画面外に行かないように
            kk_rct.move_ip(sum_mv[0], sum_mv[1])
            if check_screen(kk_rct) != (True, True):
                kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
            screen.blit(kk_img, kk_rct)

            """爆弾"""  # 爆弾の移動に関するプログラム
            bom_rect.move_ip(vx, vy)
            width, height = check_screen(bom_rect)
            if not width:
                vx *= -1
            if not height:
                vy *= -1
            screen.blit(bom_img, bom_rect)
            """加速 or 大きく"""
            # accs = [a for a in range(1, 11)]
            # if tmr % 5:
            #     for i in range(1, 11):
            #         vx += accs[i]
            #         vy += accs[i]


            """ゲームオーバー"""
            if kk_rct.colliderect(bom_rect):    # こうかとんと爆弾が当たった時の処理
                mode = False    # モード切り替え
        else:
            screen.blit(bg_img, [0, 0]) # ゲームオーバー後の画面更新
            screen.blit(dmg_kk, [WIDTH/2-50, HEIGHT/2-50])
            txt = font.render("Game Over", True, (255, 0, 0))
            screen.blit(txt, [WIDTH/2-150, HEIGHT/2-100])
            pg.time.wait(300)   # ゲームの一時停止
            pg.display.update()
            time.sleep(3)
            return  # 終了処理


        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()