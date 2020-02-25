import sys
import time

import tools.utilities as ut
from gameLib.fighter import Fighter
from tools.game_pos import BreakthroughPos


class Breakthrough(Fighter):
    '''结界突破，参数mode, emyc'''

    def __init__(self, emyc=0, hwnd=0, max_tasks=30, activate=True):
        # 初始化
        Fighter.__init__(self, 'Breakthrough: ', emyc, hwnd, activate)
        self.max_tasks = max_tasks

    def valid_position(self, target_pos):
        # 获取突破位置可点击的有效区域
        return ((target_pos[0][0] + 85, target_pos[0][1] + 25), (target_pos[1][0] - 20, target_pos[1][1] - 15))

    def attack_position(self, target_pos):
        # 获取突破位置的进攻按钮
        return ((target_pos[0][0] + 165, target_pos[0][1] + 200), (target_pos[1][0] - 25, target_pos[1][1] + 125))

    def already_break(self, target_pos):
        # 判断这个目标是否已经被突破
        return self.yys.find_game_img('img\\PO.png', 1, *target_pos, point=0.8)

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

    def refresh(self):
        if not self.run:
            return
        # 等待倒计时刷新按钮激活，然后刷新
        self.yys.wait_game_img('img\\SHUA-XIN.png', max_time=300, quit=True)
        # 点击刷新按钮直到确认刷新出现
        self.click_until('刷新按钮', 'img\\QUE-REN-SHUA-XIN.png',
                         *BreakthroughPos.refresh_position)
        # 点击确认
        self.click_until('确认按钮', 'img\\QUE-REN-SHUA-XIN.png',
                         *BreakthroughPos.confirm_btn, 2, False)

    def fight_and_quit(self, target_pos, mood):
        # 点击有效位置，直到可以进攻按钮
        self.click_until('突破目标', 'img\\JIN-GONG.png', *self.valid_position(target_pos),
                         step_time=mood.get1mood() / 1000, appear=True, point=0.9)

        time.sleep(1)

        # 点击进攻，开始突破
        self.click_until('进攻', 'img\\JIN-GONG.png', *self.attack_position(target_pos), step_time=mood.get1mood() / 1000,
                         appear=False, point=0.9)

        # 检测是否进入战斗
        self.check_battle()

        # 退出战斗
        self.click_until('退出按钮', 'img\\QUE-REN-TUI-CHU.png', *BreakthroughPos.quit_btn,
                         step_time=mood.get1mood() / 1000, appear=True, point=0.9)
        self.click_until('确认退出', 'img\\QUE-REN-TUI-CHU.png', *BreakthroughPos.confirm_quit_btn,
                         step_time=mood.get1mood() / 1000, appear=False, point=0.9)

        # 检测突破结果
        result = self.check_result()
        if result == 0:
            return False

        # 点击知道结算成功
        self.click_until('结算', 'img\\JIE-JIE-TU-PO.png', *BreakthroughPos.jiesuan_position, mood.get1mood() / 1000)

        return result



    def fighting(self, target_pos, mood):
        '''
        进行指定目标突破
        :param target_pos: 突破指定目标
        :param mood: 点击频率
        :return: 成功执行返回1-成功，2-失败，发生异常返回False
        '''

        # 如果目标已经被突破，跳过
        if self.already_break(target_pos):
            self.log.writewarning("目标已被突破过了，跳过")
            return 1

        time.sleep(1)

        # 点击有效位置，直到可以进攻按钮
        self.click_until('突破目标', 'img\\JIN-GONG.png', *self.valid_position(target_pos), step_time= mood.get1mood()/1000, appear=True, point=0.9)

        time.sleep(1)

        # 点击进攻，开始突破
        self.click_until('进攻', 'img\\JIN-GONG.png', *self.attack_position(target_pos), step_time= mood.get1mood()/1000, appear=False, point=0.9)

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

        # 战斗主循环
        while self.run:
            # 最大任务数小于3就不进行下一轮了
            if self.max_tasks < 3:
                self.log.writewarning("突破任务结束")
                break
            # 检测是否在结界突破页面
            self.check_breakthrough()

            # 秒退一次，为了保持当前突破等级
            self.fight_and_quit(BreakthroughPos.target_position[8], mood)

            # 成功突破次数
            victories = 0
            # 循环突破9次，直到满足成功次数或循环结束
            for i in range(9):
                if not self.run:
                    break
                if victories >= 3:
                    self.log.writeinfo('成功突破:'+str(victories)+'次，等待新的一轮')
                    break
                result = self.fighting(BreakthroughPos.target_position[i], mood)
                if not result:
                    self.log.writewarning("强制退出脚本")
                    sys.exit(0)
                if result == 1:
                    victories += 1
                    self.max_tasks -= 1
                self.log.writewarning("当前挑战次数->" + str(i + 1) + "，当前成功突破次数->" + str(victories))

            # 刷新页面
            self.refresh()
