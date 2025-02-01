import pyxel
import random

masu = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]]

# 詰み判定を行うクラス
class Tumi:
    # 詰んでいるか詰んでいないかの判定を行うメソッド
    def hanntei(self, masu):
        # tumi=0 => 詰んでいない(まだ動ける)、tumi=1 => 詰んでいる(動けない)
        self.tumi = 1
        
        # 盤面に0が一つでもあれば「まだ詰んでいない」
        for x in range(4):
            for y in range(4):
                if masu[x][y] == 0:
                    self.tumi = 0
                    break
            if self.tumi == 0:
                break
        return self.tumi

class App:
    def __init__(self):
        pyxel.init(200, 200)
        
        self.scene = 0
        self.score = 0
        self.count = 0
        self.tumi = Tumi()

        # 色をパレットとして管理するための変数
        self.palettes = [
            {
                "bg_color": 7,      # 背景色
                "board_color": 14,  # ボード全体の色
                "cell_color": 7,    # 各マスの色
                "text_color_map": { # タイルの数字に対応した文字色
                    0: 7,
                    2: 3,
                    4: 2,
                    8: 1,
                    16: 4,
                    32: 5,
                    64: 6,
                    128: 8,
                    256: 9,
                    512: 10,
                    1024: 11,
                    2048: 12,
                    "default": 0
                },
                "title_button_color": 8,
                "gameover_rect_color": 12
            },
            {
                "bg_color": 0, 
                "board_color": 1,
                "cell_color": 13,
                "text_color_map": {
                    0: 13,
                    2: 6,
                    4: 10,
                    8: 11,
                    16: 14,
                    32: 15,
                    64: 5,
                    128: 8,
                    256: 9,
                    512: 3,
                    1024: 4,
                    2048: 2,
                    "default": 7
                },
                "title_button_color": 5,
                "gameover_rect_color": 8
            }
        ]
        # 現在選択中のパレットを示すインデックス
        self.current_palette_idx = 0

        pyxel.run(self.update, self.draw)

    @property
    def current_palette(self):
        """ 現在のパレットを返す簡単なプロパティ """
        return self.palettes[self.current_palette_idx]

    def update(self):
        # --------------------------------------
        # ② Cキー押下でパレットを切り替える
        # --------------------------------------
        if pyxel.btnp(pyxel.KEY_C):
            # パレットを次に回して、範囲をはみ出したら0に戻す
            self.current_palette_idx = (self.current_palette_idx + 1) % len(self.palettes)

        # シーン0: タイトル画面
        if self.scene == 0:
            pyxel.mouse(True)
            if (50 <= pyxel.mouse_x <= 150) and (50 <= pyxel.mouse_y <= 150) and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.scene = 1
                pyxel.mouse(False)
        
        # シーン1: ゲーム中
        if self.scene == 1:
            if self.count == 0:
                for x in range(4):
                    for y in range(4):
                        masu[x][y] = 0
                self.score = 0
                self.score += 1
                masu[pyxel.rndi(0, 3)][pyxel.rndi(0, 3)] = int(pyxel.rndi(11, 20) / 10) * 2
                self.count += 1

            # 入力処理
            self.handle_input()

            # 2048を超えたらシーン3(クリア)
            for x in range(4):
                for y in range(4):
                    if masu[x][y] >= 2048:
                        self.scene = 3

        # シーン2: ゲームオーバー
        if self.scene == 2:
            pyxel.mouse(True)
            if (0 <= pyxel.mouse_x <= 200) and (0 <= pyxel.mouse_y <= 200) and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.scene = 0
                self.count = 0
                pyxel.mouse(False)

    def handle_input(self):
        if pyxel.btnp(pyxel.KEY_RIGHT):
            self.move_right()
        elif pyxel.btnp(pyxel.KEY_LEFT):
            self.move_left()
        elif pyxel.btnp(pyxel.KEY_UP):
            self.move_up()
        elif pyxel.btnp(pyxel.KEY_DOWN):
            self.move_down()

    def move_right(self):
        self.score += 1
        for x in range(4):
            y = 0
            for y in range(3):
                while masu[x][2 - y] >= 2 and masu[x][3 - y] == 0:
                    masu[x][3 - y] = masu[x][2 - y]
                    masu[x][2 - y] = 0
                    y -= 1
                    if y == -1:
                        break
        for x in range(4):
            for y in range(3):
                if masu[x][3 - y] == masu[x][2 - y]:
                    masu[x][3 - y] *= 2
                    masu[x][2 - y] = 0
        for x in range(4):
            y = 0
            for y in range(3):
                while masu[x][2 - y] >= 2 and masu[x][3 - y] == 0:
                    masu[x][3 - y] = masu[x][2 - y]
                    masu[x][2 - y] = 0
                    y -= 1
                    if y == -1:
                        break
        self.tumi.tumi = self.tumi.hanntei(masu)
        self.spawn_new_tile()

    def move_left(self):
        self.score += 1
        for x in range(4):
            y = 0
            for y in range(3):
                while masu[x][y + 1] >= 2 and masu[x][y] == 0:
                    masu[x][y] = masu[x][y + 1]
                    masu[x][y + 1] = 0
                    y -= 1
                    if y == -1:
                        break
        for x in range(4):
            for y in range(3):
                if masu[x][y] == masu[x][y + 1]:
                    masu[x][y] *= 2
                    masu[x][y + 1] = 0
        for x in range(4):
            y = 0
            for y in range(3):
                while masu[x][y + 1] >= 2 and masu[x][y] == 0:
                    masu[x][y] = masu[x][y + 1]
                    masu[x][y + 1] = 0
                    y -= 1
                    if y == -1:
                        break
        self.tumi.tumi = self.tumi.hanntei(masu)
        self.spawn_new_tile()

    def move_up(self):
        self.score += 1
        for y in range(4):
            x = 0
            for x in range(3):
                while masu[x + 1][y] >= 2 and masu[x][y] == 0:
                    masu[x][y] = masu[x + 1][y]
                    masu[x + 1][y] = 0
                    x -= 1
                    if x == -1:
                        break
        for y in range(4):
            for x in range(3):
                if masu[x][y] == masu[x + 1][y]:
                    masu[x][y] *= 2
                    masu[x + 1][y] = 0
        for y in range(4):
            x = 0
            for x in range(3):
                while masu[x + 1][y] >= 2 and masu[x][y] == 0:
                    masu[x][y] = masu[x + 1][y]
                    masu[x + 1][y] = 0
                    x -= 1
                    if x == -1:
                        break
        self.tumi.tumi = self.tumi.hanntei(masu)
        self.spawn_new_tile()

    def move_down(self):
        self.score += 1
        for y in range(4):
            x = 0
            for x in range(3):
                while masu[2 - x][y] >= 2 and masu[3 - x][y] == 0:
                    masu[3 - x][y] = masu[2 - x][y]
                    masu[2 - x][y] = 0
                    x -= 1
                    if x == -1:
                        break
        for y in range(4):
            for x in range(3):
                if masu[3 - x][y] == masu[2 - x][y]:
                    masu[3 - x][y] *= 2
                    masu[2 - x][y] = 0
        for y in range(4):
            x = 0
            for x in range(3):
                while masu[2 - x][y] >= 2 and masu[3 - x][y] == 0:
                    masu[3 - x][y] = masu[2 - x][y]
                    masu[2 - x][y] = 0
                    x -= 1
                    if x == -1:
                        break
        self.tumi.tumi = self.tumi.hanntei(masu)
        self.spawn_new_tile()

    def spawn_new_tile(self):
        # 詰み判定
        self.tumi.tumi = self.tumi.hanntei(masu)
        # 詰んでいなければ新しいタイルを生成
        if self.tumi.tumi == 0:
            while True:
                g = pyxel.rndi(0, 3)
                h = pyxel.rndi(0, 3)
                if masu[g][h] == 0:
                    masu[g][h] = int(pyxel.rndi(11, 20) / 10) * 2
                    break
        else:
            self.scene = 2
            pyxel.mouse(True)

    def draw(self):
        # パレットを取得
        p = self.current_palette

        # シーンに応じた描画
        if self.scene == 0:
            pyxel.cls(p["bg_color"])
            pyxel.rect(50, 50, 100, 100, p["title_button_color"])
            pyxel.text(90, 97, "start", 0)
            pyxel.text(10, 180, "Press 'C' to change palette", 0)

        elif self.scene == 1:
            # 背景塗りつぶし
            pyxel.cls(p["bg_color"])

            # ボードを塗る
            pyxel.rect(20, 20, 160, 160, p["board_color"])

            # マスを描画
            for a in range(4):
                for b in range(4):
                    pyxel.rect(32 + 37*a, 32 + 37*b, 25, 25, p["cell_color"])

            pyxel.text(5, 5, "2024", 3)
            pyxel.text(80, 5, f"Score: {self.score}", 0)

            # タイルの数字を描画
            for x in range(4):
                for y in range(4):
                    val = masu[y][x]
                    # タイルの数字によって色を変える(定義がなければ"default")
                    color = p["text_color_map"].get(val, p["text_color_map"]["default"])

                    # 各桁数に合わせて微調整している(文字ずれ防止)
                    if val < 10:
                        px = 42
                    elif val < 100:
                        px = 38
                    else:
                        px = 34

                    pyxel.text(px + 37*x, 42 + 37*y, str(val), color)

        elif self.scene == 2:
            pyxel.cls(p["bg_color"])
            pyxel.rect(50, 50, 100, 100, p["gameover_rect_color"])
            pyxel.text(80, 97, "game over", 0)
            pyxel.text(80, 105, ("score:" + str(self.score)), 0)

        elif self.scene == 3:
            pyxel.cls(p["bg_color"])
            pyxel.rect(50, 50, 100, 100, p["gameover_rect_color"])
            pyxel.text(80, 97, "game clear", 0)
            pyxel.text(80, 105, ("score:" + str(self.score)), 0)

# 実行
App()