from gameLib.fighter import Fighter
from tools.game_pos import CommonPos, GhostPos

import random
import time
import tools.utilities as ut

class Ghost(Fighter):
    '''百鬼夜行单刷程序，参数mode, emyc'''

    def __init__(self, emyc=0, hwnd=0):
        # 初始化
        Fighter.__init__(self, 'Ghost: ', emyc, hwnd)

    def choose_king(self):
        # 随机选择一个鬼王
        i = random.randint(0, 2)
        # 点击鬼王，直到选中为止
        self.click_until('选择鬼王', 'img\\YA.png', *GhostPos.king_position[i])

    def fighting(self, mood2):
        # 调整豆子到10，快速砸完
        self.set_beans()

        while self.run and not self.check_over():
            # 同一位置连击次数
            combo = random.randint(1,5)
            # 随机点击位置
            x = random.randint(GhostPos.ghost_position[0][0],GhostPos.ghost_position[1][0])
            y = random.randint(GhostPos.ghost_position[0][1],GhostPos.ghost_position[1][1])
            for i in range(combo):
                self.yys.mouse_click_bg((x + random.randint(-10,10), y + random.randint(-10,10)))
                time.sleep(random.randint(300,800)/1000)
            mood2.moodsleep()

    def set_beans(self):
        # 调整豆子数为10
        # 坐标偏移量
        x_shift = random.randint(-10, 10)
        y_shift = random.randint(-10, 10)
        x0 = GhostPos.beans_position[0] + x_shift
        y0 = GhostPos.beans_position[1] + y_shift
        # 拖拽长度
        x_move = random.randint(200, 400)
        y_move = random.randint(-50, 10)
        x1 = x0 + x_move
        y1 = y0 + y_move

        self.yys.mouse_drag_bg((x0, y0), (x1, y1))


    def check_over(self):
        '''
        判断砸百鬼是否结束，回到开始的页面就算结束
            :return: 结束返回True，未结束返回False
        '''
        scene_now = self.get_scene_baigui()
        self.log.writeinfo(self.name + '目前场景：' + str(scene_now))

        if scene_now == 0:
            return False
        elif scene_now == 1:
            return True
        else:
            self.click_until('结算', 'img\\BAI-GUI-YE-XING.png', *GhostPos.jiesuan_position)
            return True


    def start(self):

        # 设定点击疲劳度
        mood2 = ut.Mood(2)

        # 战斗主循环
        while self.run:
            # 检测是否在百鬼页面
            self.check_ghost()

            # 点击进入，直到进入鬼王选择页面
            self.click_until('进入按钮', 'img\\JIN-RU.png', *
                GhostPos.jinru_btn, mood2.get1mood() / 1000, False)

            # 选中鬼王
            self.choose_king()

            # 点击开始，进入砸百鬼页面
            self.click_until('开始按钮', 'img\\KAI-SHI.png', *
                GhostPos.start_btn, mood2.get1mood() / 1000, False)

            # 开始动画比较久，多等待一会
            time.sleep(random.randint(3,5))

            # 砸百鬼
            self.fighting(mood2)



