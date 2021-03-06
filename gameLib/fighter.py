import configparser
import logging
import random
import sys
import time

import win32gui

from gameLib.game_ctl import GameControl
from tools.game_pos import TansuoPos
from tools.logsystem import WriteLog


class Fighter:

    def __init__(self, name='', emyc=0, hwnd=0, activate=True):
        '''
        初始化
            ：param name='': 打手名称
            : param emyc=0: 点怪设置：0-不点怪
            : param hwnd=0: 指定窗口句柄：0-否；其他-窗口句柄
            : param activate=True: 是否激活窗口，支线任务不需要激活
        '''
        # 初始参数
        self.emyc = emyc
        self.name = name
        self.run = True

        # 读取配置文件
        conf = configparser.ConfigParser()
        conf.read('conf.ini')
        quit_game_enable = conf.getboolean('watchdog', 'watchdog_enable')
        self.max_op_time = conf.getint('watchdog', 'max_op_time')
        self.max_win_time = conf.getint('watchdog', 'max_win_time')

        # 启动日志
        self.log = WriteLog()

        # 绑定窗口
        if hwnd == 0:
            hwnd = win32gui.FindWindow('Win32Window0', u'阴阳师-网易游戏')
            # hwnd = win32gui.FindWindow('Qt5QWindowIcon', '夜神模拟器')
            # hwnd = win32gui.FindWindowEx(hwnd, 0, 'Qt5QWindowIcon', 'ScreenBoardClassWindow')
        self.yys = GameControl(hwnd, quit_game_enable)
        self.log.writeinfo(self.name + '绑定窗口成功')
        self.log.writeinfo(self.name + str(hwnd))

        if activate:
            # 激活窗口
            self.yys.activate_window()
            self.log.writeinfo(self.name + '激活窗口成功')
        time.sleep(0.5)

    def check_battle(self):
        # 检测是否进入战斗
        self.log.writeinfo(self.name + '检测是否进入战斗')
        self.yys.wait_game_img('img\\ZI-DONG.png', self.max_win_time)
        self.log.writeinfo(self.name + '已进入战斗')

    def check_end(self):
        # 检测是否打完
        self.log.writeinfo(self.name + '检测是战斗是否结束')
        self.yys.wait_game_img_disappear('img\\XIAO-XI.png', self.max_win_time)
        self.log.writeinfo(self.name + "战斗结束")

    def click_monster(self):
        # 点击怪物
        pass

    def click_until(self, tag, img_path, pos, pos_end=None, step_time=None, appear=True, point=0.97):
        '''
        在某一时间段内，后台点击鼠标，直到出现某一图片出现或消失
            :param tag: 按键名
            :param img_path: 图片路径
            :param pos: (x,y) 鼠标单击的坐标
            :param pos_end=None: (x,y) 若pos_end不为空，则鼠标单击以pos为左上角坐标pos_end为右下角坐标的区域内的随机位置
            :step_time=0.5: 查询间隔
            :appear: 图片出现或消失：Ture-出现；False-消失
            :point: 判定图片的的识别概率
            :return: 成功返回True, 失败退出游戏
        '''
        # 在指定时间内反复监测画面并点击
        start_time = time.time()
        while time.time()-start_time <= self.max_op_time and self.run:
            result = self.yys.find_game_img(img_path, point=point)
            if not appear:
                result = not result
            if result:
                self.log.writeinfo(self.name + '点击 ' + tag + ' 成功')
                return True
            else:
                # 点击指定位置并等待下一轮
                self.yys.mouse_click_bg(pos, pos_end)
                self.log.writeinfo(self.name + '点击 ' + tag)
            if step_time == None:
                time.sleep(random.randint(1, 3))
            else:
                time.sleep(step_time)
        self.log.writewarning(self.name + '点击 ' + tag + ' 失败!')

        # 提醒玩家点击失败，并在5s后退出
        self.yys.activate_window()
        time.sleep(5)
        # self.yys.quit_game()
        self.log.writewarning("强制退出脚本")
        sys.exit(0)

    def activate(self):
        self.log.writewarning(self.name + '启动脚本')
        self.run = True
        self.yys.run = True

    def deactivate(self):
        self.log.writewarning(self.name + '手动停止脚本')
        self.run = False
        self.yys.run = False

    def slide_x_scene(self, distance):
        '''
        水平滑动场景
            :return: 成功返回True; 失败返回False
        '''
        x0 = random.randint(distance + 10, 1126)
        x1 = x0 - distance
        y0 = random.randint(436, 486)
        y1 = random.randint(436, 486)
        self.yys.mouse_drag_bg((x0, y0), (x1, y1))
        logging.info(self.name + '水平滑动界面')

    def get_scene(self):
        '''
        识别当前场景
            :return: 返回场景名称:1-庭院; 2-探索界面; 3-章节界面; 4-探索内; 5-结界突破; 6-觉醒页面; 7-御魂页面
        '''
        # 拒绝悬赏
        self.yys.rejectbounty()

        # 分别识别庭院、探索、章节页、探索内
        maxVal, maxLoc = self.yys.find_multi_img(
            'img\\JIA-CHENG.png', 'img\\JUE-XING.png', 'img\\TAN-SUO.png', 'img\\YING-BING.png',
            'img\\JIE-JIE-TU-PO.png', 'img\\LEI-QI-LIN.png', 'img\\BA-QI-DA-SHE.png')

        scene_cof = max(maxVal)
        if scene_cof > 0.97:
            scene = maxVal.index(scene_cof)
            return scene + 1
        else:
            return 0

    def get_scene_baigui(self):
        '''
        识别百鬼结束的画面
            :return: 返回场景名称：1-百鬼首页，2-结算页面
        '''
        # 拒绝悬赏
        self.yys.rejectbounty()

        # 分别识别百鬼首页、结算页面
        maxVal, maxLoc = self.yys.find_multi_img(
            'img\\BAI-GUI-YE-XING.png', 'img\\BAI-GUI-QI-YUE-SHU.png')

        scene_cof = max(maxVal)
        if scene_cof > 0.97:
            scene = maxVal.index(scene_cof)
            return scene + 1
        else:
            return 0

    def get_scene_breakthrough(self):
        '''
        识别结界突破结果
            :return: 返回场景名称：1-成功，2-失败
        '''
        # 拒绝悬赏
        self.yys.rejectbounty()

        # 分别识别百鬼首页、结算页面
        maxVal, maxLoc = self.yys.find_multi_img(
            'img\\SHENG-LI.png', 'img\\SHI-BAI.png')

        scene_cof = max(maxVal)
        if scene_cof > 0.97:
            scene = maxVal.index(scene_cof)
            return scene + 1
        else:
            return 0

    def switch_to_scene(self, scene):
        '''
        切换场景
            :param scene: 需要切换到的场景:1-庭院; 2-探索界面; 3-章节界面; 4-探索内; 5-结界突破; 6-觉醒页面; 7-御魂页面
            :return: 切换成功返回True；切换失败直接退出
        '''
        scene_now = self.get_scene()
        logging.info(self.name + '目前场景：' + str(scene_now))
        if scene_now == scene:
            return True
        if scene_now == 1:
            # 庭院中
            if scene == 2 or scene == 3 or scene == 4 or scene == 5 or scene == 6 or scene == 7:
                # 先将界面划到最右边
                self.slide_x_scene(800)
                time.sleep(2)
                self.slide_x_scene(800)

                # 点击探索灯笼进入探索界面
                self.click_until('探索灯笼', 'img\\JUE-XING.png', *
                                 TansuoPos.tansuo_denglong)

        if scene_now == 2:
            # 探索界面
            if scene == 3 or scene == 4:
                # 点击最后章节
                self.click_until('最后章节', 'img\\TAN-SUO.png',
                                 *TansuoPos.last_chapter)

            if scene == 5:
                # 点击结界突破
                self.click_until('结界突破', 'img\\JIE-JIE-TU-PO.png',
                                 *TansuoPos.jiejie_tupo)

            if scene == 6:
                # 点击觉醒按钮
                self.click_until('觉醒按钮', 'img\\JUE-XING.png', *TansuoPos.juexing_cailiao, appear=False)

                # 点击雷麒麟
                self.click_until('雷麒麟', 'img\\LEI-QI-LIN.png', *TansuoPos.leiqilin)

            if scene == 7:
                # 点击御魂按钮
                self.click_until('觉醒按钮', 'img\\JUE-XING.png', *TansuoPos.yuhun, appear=False)

                # 点击八岐大蛇
                self.click_until('八岐大蛇', 'img\\BA-QI-DA-SHE.png', *TansuoPos.baqidashe)

        if scene_now == 3:
            # 章节界面
            if scene == 4:
                # 点击探索按钮
                self.click_until('探索按钮', 'img\\YING-BING.png',
                                 *TansuoPos.tansuo_btn)

            if scene == 2 or scene == 5 or scene == 6 or scene == 7:
                # 点击关闭按钮
                self.click_until('退出章节', 'img\\JUE-XING.png',
                                 *TansuoPos.quit_zhangjie_btn)

        if scene_now == 4:
            # 探索内
            if scene == 3 or scene == 2 or scene == 5 or scene == 6 or scene == 7:
                # 点击退出探索
                self.click_until('退出按钮', 'img\\QUE-REN.png',
                                 *TansuoPos.quit_btn)

                # 点击确认
                self.click_until('确认按钮', 'img\\QUE-REN.png',
                                 *TansuoPos.confirm_btn, 2, False)

        if scene_now == 5:
            # 结界突破页面
            if scene == 2 or scene == 3 or scene == 4 or scene == 6 or scene == 7:
                # 点击关闭按钮
                self.click_until('退出突破', 'img\\JUE-XING.png',
                                 *TansuoPos.quit_tupo_btn)

        if scene_now == 6 or scene_now == 7:
            # 点击退出
            self.click_until('退出按钮', 'img\\JUE-XING.png', *TansuoPos.quit_btn)

        # 递归
        self.switch_to_scene(scene)
