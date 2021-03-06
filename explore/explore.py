import configparser
import logging
import random
import time

import tools.utilities as ut
from breakthrough.breakthrough import Breakthrough
from gameLib.fighter import Fighter
from tools.game_pos import CommonPos, TansuoPos


class ExploreFight(Fighter):
    def __init__(self, max_tasks=200, activate=True):
        # 初始化
        Fighter.__init__(self, activate=activate)
        self.max_tasks = max_tasks

        # 读取配置文件
        conf = configparser.ConfigParser()
        conf.read('conf.ini')
        self.fight_boss_enable = conf.getboolean('explore', 'fight_boss_enable')
        self.tupo_enable = conf.getboolean('explore', 'tupo_enable')
        self.slide_shikigami = conf.getboolean('explore', 'slide_shikigami')
        self.slide_shikigami_progress = conf.getint('explore', 'slide_shikigami_progress')
        self.zhunbei_delay = conf.getint('explore', 'zhunbei_delay')

    def next_scene(self):
        '''
        移动至下一个场景，每次移动(300-500)像素
        '''
        x0 = random.randint(510, 1126)
        move = random.randint(300, 500)
        x1 = x0 - move
        y0 = random.randint(110, 210)
        y1 = random.randint(110, 210)
        self.yys.mouse_drag_bg((x0, y0), (x1, y1))

    def last_scene(self):
        '''
        移动至上一个场景，每次移动(200-300)像素
        '''
        x0 = random.randint(510, 1126)
        move = random.randint(200, 300)
        x1 = x0 + move
        y0 = random.randint(110, 210)
        y1 = random.randint(110, 210)
        self.yys.mouse_drag_bg((x0, y0), (x1, y1))

    def check_exp_full(self):
        '''
        检查狗粮经验，并自动换狗粮
        '''
        # 狗粮经验判断, gouliang1是中间狗粮，gouliang2是右边狗粮
        gouliang1 = self.yys.find_game_img(
            'img\\MAN1.png', 1, *TansuoPos.gouliang_middle, 1)
        gouliang2 = self.yys.find_game_img(
            'img\\MAN2.png', 1, *TansuoPos.gouliang_right, 1)

        # print(gouliang1)
        # print(gouliang2)

        # 如果都没满则退出
        if not gouliang1 and not gouliang2:
            return

        # 开始换狗粮
        while self.run:
            # 点击狗粮位置
            self.yys.mouse_click_bg(*TansuoPos.change_monster)
            if self.yys.wait_game_img('img\\QUAN-BU.png', 3, False):
                break
        time.sleep(2)

        # 点击“全部”选项
        self.yys.mouse_click_bg(*TansuoPos.quanbu_btn)
        time.sleep(2)

        # 点击“N”卡
        self.yys.mouse_click_bg(*TansuoPos.n_tab_btn)
        time.sleep(2)

        # 拖放进度条
        if self.slide_shikigami:
            # 读取坐标范围
            star_x = TansuoPos.n_slide[0][0]
            end_x = TansuoPos.n_slide[1][0]
            length = end_x - star_x

            # 计算拖放范围
            pos_end_x = int(star_x + length/100*self.slide_shikigami_progress)
            pos_end_y = TansuoPos.n_slide[0][1]

            self.yys.mouse_drag_bg(
                TansuoPos.n_slide[0], (pos_end_x, pos_end_y))

        # 更换狗粮
        if gouliang1:
            time.sleep(2)
            self.yys.mouse_drag_bg((309, 520), (554, 315))
        if gouliang2:
            time.sleep(2)
            self.yys.mouse_drag_bg((191, 520), (187, 315))
        time.sleep(2)

    def find_exp_moster(self):
        '''
        寻找经验怪
            return: 成功返回经验怪的攻打图标位置；失败返回-1
        '''
        # 查找经验图标
        exp_pos = self.yys.find_color(
            ((2, 205), (1127, 545)), (140, 122, 44), 2)
        if exp_pos == -1:
            return -1

        # 查找经验怪攻打图标位置
        find_pos = self.yys.find_game_img(
            'img\\FIGHT.png', 1, (exp_pos[0]-150, exp_pos[1]-250), (exp_pos[0]+150, exp_pos[1]-50))
        if not find_pos:
            return -1

        # 返回经验怪攻打图标位置
        fight_pos = ((find_pos[0]+exp_pos[0]-150),
                     (find_pos[1]+exp_pos[1]-250))
        return fight_pos

    def find_boss(self):
        '''
        寻找BOSS
            :return: 成功返回BOSS的攻打图标位置；失败返回-1
        '''
        # 查找BOSS攻打图标位置
        find_pos = self.yys.find_game_img(
            'img\\BOSS.png', 1, (2, 205), (1127, 545))
        if not find_pos:
            return -1

        # 返回BOSS攻打图标位置
        fight_pos = ((find_pos[0]+2), (find_pos[1]+205))
        return fight_pos

    def disturb_action(self):
        # 随机干扰次数
        num = random.randint(0,2)
        for i in range(num):
            time.sleep(random.randint(1, 3))
            self.log.writeinfo('干扰行动')
            # 随机干扰类型
            if random.randint(0,1) == 0:
                self.next_scene()
            else:
                self.last_scene()


    def fight_moster(self, mood1, mood2):
        '''
        打经验怪
            :return: 打完普通怪返回1；打完boss返回2；未找到经验怪返回-1；未找到经验怪和boss返回-2
        '''
        while self.run:
            mood1.moodsleep()
            # 查看是否进入探索界面
            self.yys.wait_game_img('img\\YING-BING.png')
            self.log.writeinfo('进入探索页面')

            # 寻找经验怪，未找到则寻找boss，再未找到则退出
            fight_pos = self.find_exp_moster()
            boss = False
            if fight_pos == -1:
                if self.fight_boss_enable:
                    fight_pos = self.find_boss()
                    boss = True
                    if fight_pos == -1:
                        self.log.writeinfo('未找到经验怪和boss')
                        return -2
                else:
                    self.log.writeinfo('未找到经验怪')
                    return -1

            # 攻击怪
            self.yys.mouse_click_bg(fight_pos)
            if not self.yys.wait_game_img('img\\ZHUN-BEI.png', self.zhunbei_delay, False):
                break
            self.log.writeinfo('已进入战斗')
            time.sleep(1)

            # 等待式神准备
            self.yys.wait_game_color(((1024,524),(1044, 544)), (138,198,233), 30)
            logging.info('式神准备完成')

            # 检查狗粮经验
            self.check_exp_full()

            # 点击准备，直到进入战斗
            self.click_until('准备按钮', 'img\\ZI-DONG.png', *
                             TansuoPos.ready_btn, mood1.get1mood()/1000)

            #战斗结束之前一点干扰动作
            # self.disturb_action()

            # 检查是否打完
            self.check_end()
            mood2.moodsleep()

            # 在战斗结算页面,随机单机或者双击
            self.yys.mouse_click_bg(ut.firstposition())

            self.click_until('结算', 'img\\YING-BING.png',
                             *CommonPos.second_position, mood2.get1mood() / 1000, point=0.9)

            # 返回结果
            if boss:
                return 2
            else:
                return 1

    def tupo_branch(self):
        # 如果不允许进行结界突破，跳过
        if not self.tupo_enable:
            return

        # 进入章节页面
        self.switch_to_scene(3)

        # 判断突破门票是否已满
        tickets = self.yys.find_game_img('img\\TU-PO-30.png', 1, *TansuoPos.tupo_tickets)
        # 没满不进行突破
        if not tickets:
            return

        # 进入结界突破页面
        self.switch_to_scene(5)
        self.log.writeinfo('执行结界突破任务')

        # 执行3次突破任务
        tupo_fight = Breakthrough(max_tasks=3, activate=False)
        tupo_fight.start()

    def start(self):
        '''单人探索主循环'''
        mood1 = ut.Mood(2)
        mood2 = ut.Mood(3)
        while self.run:
            # 最大任务数小于等于0就不进行下一轮了
            if self.max_tasks <= 0:
                self.log.writewarning("探索任务结束")
                break
            # 进行结界突破分支任务
            self.tupo_branch()

            # 进入探索内
            self.switch_to_scene(4)

            # 开始打怪
            i = 0
            while i < 4 and self.run:
                result = self.fight_moster(mood1, mood2)
                if result == 1:
                    continue
                elif result == 2:
                    time.sleep(random.randint(2,3))
                    # 打完boss就算完成任务一次
                    self.max_tasks -= 1
                    break
                else:
                    self.log.writeinfo('移动至下一个场景')
                    self.next_scene()
                    i += 1

            # 退出探索
            self.switch_to_scene(3)
            self.log.writeinfo('结束本轮探索')
            time.sleep(random.randint(500,1500)/1000)

