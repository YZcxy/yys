from gameLib.fighter import Fighter
from tools.game_pos import CommonPos, YuhunPos
import tools.utilities as ut

import logging
import time
import configparser


class DriverFighter(Fighter):
    '''御魂战斗司机程序，参数mode, emyc'''

    def __init__(self, emyc=0, hwnd=0):
        # 初始化
        Fighter.__init__(self, 'Driver: ', emyc, hwnd)

        # 读取配置文件
        conf = configparser.ConfigParser()
        conf.read('conf.ini')
        self.mitama_click_partner_left = conf.getboolean('mitama', 'mitama_click_partner_left')
        self.mitama_click_partner_right = conf.getboolean('mitama', 'mitama_click_partner_right')

    def start(self):
        '''单人御魂司机'''
        # 设定点击疲劳度
        mood1 = ut.Mood()
        mood2 = ut.Mood()
        mood3 = ut.Mood(3)

        # 战斗主循环
        self.yys.wait_game_img('img\\KAI-SHI-ZHAN-DOU.png',
                               self.max_win_time)
        while self.run:
            # 司机点击开始战斗，需要锁定御魂阵容
            mood1.moodsleep()
            self.log.writeinfo('Driver: 点击开始战斗按钮')
            self.click_until('开始战斗按钮', 'img\\ZI-DONG.png', *
                             YuhunPos.kaishizhandou_btn, mood2.get1mood()/1000)
            self.log.writeinfo('Driver: 已进入战斗')

            # 已经进入战斗，司机自动点怪
            self.click_monster()

            # 已经进入战斗，乘客自动点式神
            if self.mitama_click_partner_left:
                self.click_until('标记左边式神', 'IMG\\GREEN-JIAN-TOU.png',
                                 *CommonPos.left_partner_position, mood3.get1mood()/1000)
            if self.mitama_click_partner_right:
                self.click_until('标记右边式神', 'IMG\\GREEN-JIAN-TOU.png',
                                 *CommonPos.right_partner_position, mood3.get1mood()/1000)

            # 检测是否打完
            self.check_end()
            mood2.moodsleep()

            # 在战斗结算页面
            self.yys.mouse_click_bg(ut.firstposition())
            self.click_until('结算1', 'img\\JIN-BI.png',
                             *CommonPos.second_position, mood3.get1mood()/1000)
            self.click_until('结算2', 'img\\JIN-BI.png',
                             *CommonPos.second_position, mood3.get1mood()/1000, False)

            # 等待下一轮
            logging.info('Driver: 等待下一轮')
            start_time = time.time()
            while time.time() - start_time <= 20 and self.run:
                if(self.yys.wait_game_img('img\\KAI-SHI-ZHAN-DOU.png', 1, False)):
                    self.log.writeinfo('Driver: 进入队伍')
                    break

                # 点击默认邀请
                if self.yys.find_game_img('img\\ZI-DONG-YAO-QING.png'):
                    self.yys.mouse_click_bg((497, 319))
                    time.sleep(0.2)
                    self.yys.mouse_click_bg((674, 384))
                    self.log.writeinfo('Driver: 自动邀请')
