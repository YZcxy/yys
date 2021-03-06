import configparser

import tools.utilities as ut
from gameLib.fighter import Fighter
from tools.game_pos import CommonPos, YuhunPos


class SingleFight(Fighter):
    '''单人御魂战斗，参数done, emyc'''

    def __init__(self, done=1, emyc=0, max_tasks=200, activate=True):
        # 初始化
        Fighter.__init__(self, '', emyc, activate=activate)
        self.max_tasks = max_tasks

        # 读取配置文件
        conf = configparser.ConfigParser()
        conf.read('conf.ini')
        self.mitama_click_partner_left = conf.getboolean('mitama', 'mitama_click_partner_left')
        self.mitama_click_partner_right = conf.getboolean('mitama', 'mitama_click_partner_right')

    def start(self):
        '''单人战斗主循环'''
        mood1 = ut.Mood()
        mood2 = ut.Mood()
        mood3 = ut.Mood(3)
        while self.run:
            # 最大任务数小于等于0就不进行下一轮了
            if self.max_tasks <= 0:
                self.log.writewarning("御魂任务结束")
                break
            # 在御魂主选单，点击“挑战”按钮, 需要使用“阵容锁定”！
            self.yys.wait_game_img('img\\TIAO-ZHAN.png',
                                   self.max_win_time)
            mood1.moodsleep()
            self.click_until('挑战按钮', 'img\\TIAO-ZHAN.png', *YuhunPos.tiaozhan_btn, appear=False)

            # 检测是否进入战斗
            self.check_battle()

            # 在战斗中，自动点怪
            self.click_monster()

            # 已经进入战斗，乘客自动点式神
            if self.mitama_click_partner_left:
                self.click_until('标记左边式神', 'IMG\\GREEN-JIAN-TOU.png',
                                 *CommonPos.left_partner_position, mood3.get1mood() / 1000)
            if self.mitama_click_partner_right:
                self.click_until('标记右边式神', 'IMG\\GREEN-JIAN-TOU.png',
                                 *CommonPos.right_partner_position, mood3.get1mood() / 1000)

            # 检测是否打完
            self.check_end()
            mood2.moodsleep()

            # 在战斗结算页面
            self.yys.mouse_click_bg(ut.firstposition())
            self.click_until('结算', 'img\\TIAO-ZHAN.png',
                             *CommonPos.second_position, mood3.get1mood()/1000)
            self.log.writeinfo("回到御魂选择界面")
            self.max_tasks -= 1
