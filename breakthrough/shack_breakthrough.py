from gameLib.fighter import Fighter

from tools.game_pos import CommonPos, BreakthroughPos


import tools.utilities as ut
import time
import sys
import random

class ShackBreakthrough(Fighter):
    '''寮突破，参数mode, emyc'''

    def __init__(self, emyc=0, hwnd=0):
        # 初始化
        Fighter.__init__(self, 'ShackBreakthrough: ', emyc, hwnd)

    def valid_position(self, target_pos):
        # 获取突破位置可点击的有效区域
        return ((target_pos[0][0] + 85, target_pos[0][1] + 25), (target_pos[1][0] - 20, target_pos[1][1] - 15))

    def attack_position(self, target_pos):
        # 获取突破位置的进攻按钮
        return ((target_pos[0][0] + 165, target_pos[0][1] + 200), (target_pos[1][0] - 25, target_pos[1][1] + 125))

    def already_lose(self, target_pos):
        # 判断这个目标是否已经挑战失败
        return self.yys.find_game_img('img\\TU-PO-SHI-BAI.png', 1, *target_pos, point=0.8)

    def already_break(self, target_pos):
        # 判断这个目标是否已经被突破
        return self.yys.find_game_img('img\\PO.png', 1, *target_pos, point=0.8)

    def reset_slider(self):
        # 重置进度条到最上面
        x0 = random.randint(986, 1011)
        x1 = random.randint(986, 1011)

        y0 = random.randint(566, 583)
        move = random.randint(513, 543)
        y1 = y0 - move
        self.yys.mouse_drag_bg((x0, y0), (x1, y1))

    def drag_slider(self, move):
        # 拖拽一次，130 到 200范围
        x0 = random.randint(520, 920)
        x1 = random.randint(520, 920)

        y0 = random.randint(300, 500)
        y1 = y0 - move
        self.yys.mouse_drag_bg((x0, y0), (x1, y1))

    def drag_refresh(self, last_move, mood):
        '''
        通过拖拽的方式刷新寮突破页面
        :param last_move:  上次的偏移量
        :return: 拖拽完成后的偏移量
        '''

        # 判断是否已经拉到了底部
        buttom = self.yys.find_game_img('img\\DI-BU.png')
        if buttom:
            # 回归进度条
            self.reset_slider()
            return 0
        else:
            account = random.randint(1, 3) # 随机拖拽次数
            total_move = 0   # 拖拽总偏移
            for i in range(account):
                r_move = random.randint(130, 200)
                total_move += r_move
                # 拖拽一次
                self.drag_slider(r_move)
                mood.moodsleep()

            cur_move = total_move + last_move  # 这次一共的偏移加上上次的偏移
            while cur_move >= 120:
                cur_move -= 120

            return cur_move

    def offset_move(self, move):
        '''
        将所有的坐标进行偏移运算
        :param move: 偏移量
        :return: 偏移后的位置
        '''
        offset_position = []
        for i in range(8):
            temp = ((BreakthroughPos.shack_target_position[i][0][0], BreakthroughPos.shack_target_position[i][0][1] + move),
                    (BreakthroughPos.shack_target_position[i][1][0], BreakthroughPos.shack_target_position[i][1][1] + move))
            offset_position.append(temp)

        return offset_position


    def check_breakthrough(self):
        # 检测是否在结界突破页面
        self.log.writeinfo(self.name + '检测是否在结界突破页面')
        self.yys.wait_game_img('img\\JIE-JIE-TU-PO.png', self.max_win_time)
        self.log.writeinfo(self.name + "页面正确，进入下一步")

    def check_result(self):
        '''
        检测突破结果
        :return: 0-异常 1-成功，2-失败
        '''
        # 等待突破结束
        self.log.writeinfo('等待突破结束')
        self.yys.wait_multi_game_img('img\\SHENG-LI.png', 'img\\SHI-BAI.png', max_time=180)
        self.log.writeinfo('突破结束')
        # 获取突破结果
        result = self.get_scene_breakthrough()
        self.log.writeinfo('突破结果为：'+ str(result))
        return result

    def fighting(self, target_pos, mood):


        # 如果目标已经挑战失败，跳过
        if self.already_lose(target_pos) or self.already_break(target_pos):
            self.log.writewarning("目标已经挑战失败或已被攻破，跳过")
            return 2

        time.sleep(1)

        # 点击有效位置，直到可以进攻按钮
        self.click_until('突破目标', 'img\\JIN-GONG.png', *self.valid_position(target_pos),
                         step_time=mood.get1mood() / 1000, appear=True, point=0.9)

        time.sleep(2)

        # 点击进攻，开始突破
        self.click_until('进攻', 'img\\JIN-GONG.png', *self.attack_position(target_pos),
                         step_time=mood.get1mood() / 1000, appear=False, point=0.9)

        # 检测是否进入战斗
        self.check_battle()

        # 检测突破结果
        result = self.check_result()
        if result == 0:
            return False

        # 点击知道结算成功
        self.click_until('结算', 'img\\JIE-JIE-TU-PO.png', *BreakthroughPos.jiesuan_position, mood.get1mood() / 1000)

        return result


    def start(self):
        # 设定点击疲劳度
        mood = ut.Mood(3)

        # 每次拖拽刷新页面，会产生与目标位置不同的偏移量
        offset = 0

        # 战斗主循环
        while self.run:
            # 检测是否在结界突破页面
            self.check_breakthrough()

            offset_position = self.offset_move(offset)

            # 循环突破4次，直到满足成功次数或循环结束
            # 为什么只挑战4组呢？ 因为最下面四组进攻按钮的位置有可能到上方来了
            i = 0
            while i < 4:
                # 突破目标
                result = self.fighting(offset_position[i], mood)
                if not result:
                    self.log.writewarning("强制退出脚本")
                    sys.exit(0)
                # 只有突破失败才会换下一个目标，成功的话还在这个位置继续突破
                if result == 2:
                    self.log.writewarning("目标突破失败，切换下一个")
                    i += 1

            self.log.writewarning("任务完成，刷新下一页")
            offset = self.drag_refresh(offset, mood)





