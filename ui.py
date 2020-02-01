import configparser
import ctypes
import logging
import sys
import threading

from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QApplication, QMainWindow

from Ui_onmyoji import Ui_MainWindow
from breakthrough.breakthrough import Breakthrough
from breakthrough.shack_breakthrough import ShackBreakthrough
from explore.explore import ExploreFight
from ghost.ghost import Ghost
from mitama.dual import DualFighter
from mitama.fighter_driver import DriverFighter
from mitama.fighter_passenger import FighterPassenger
from mitama.single_fight import SingleFight
from tasks.task import Task


def is_admin():
    # UAC申请，获得管理员权限
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

class GuiLogger(logging.Handler):
    def emit(self, record):
        self.edit.append(self.format(record))  # implementation of append_line omitted
        self.edit.moveCursor(QTextCursor.End)

class MyMainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(MyMainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.textEdit.ensureCursorVisible()
        
        h = GuiLogger()
        h.edit = self.ui.textEdit
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        logger.addHandler(h)

    def set_conf(self, conf, section):
        '''
        设置参数至配置文件
        '''
        # 一般参数
        conf.set('watchdog', 'watchdog_enable',
                 str(self.ui.checkBox.isChecked()))
        conf.set('watchdog', 'max_win_time', str(self.ui.lineEdit.text()))
        conf.set('watchdog', 'max_op_time', str(self.ui.lineEdit_2.text()))

        # 御魂参数
        if section == 0 or section == 4:
            # 御魂
            conf.set('mitama', 'mitama_click_partner_left',
                     str(self.ui.mitama_click_partner_left.isChecked()))
            conf.set('mitama', 'mitama_click_partner_right',
                     str(self.ui.mitama_click_partner_right.isChecked()))

        # 探索参数
        if section == 1 or section == 4:
            # 探索
            conf.set('explore', 'fight_boss_enable',
                     str(self.ui.checkBox_2.isChecked()))
            conf.set('explore', 'tupo_enable',
                     str(self.ui.checkBox_4.isChecked()))
            conf.set('explore', 'slide_shikigami',
                     str(self.ui.checkBox_3.isChecked()))
            conf.set('explore', 'slide_shikigami_progress',
                     str(self.ui.horizontalSlider.value()))
            conf.set('explore', 'zhunbei_delay',
                     str(self.ui.lineEdit_3.text()))


        # 百鬼夜行参数
        if section == 2 or section == 4:
            pass

        # 结界突破参数
        if section == 3 or section == 4:
            pass

        # 专项任务参数
        if section == 4:
            conf.set('task', 'tansuo',
                     str(self.ui.lineEdit_4.text()))
            conf.set('task', 'yuhun',
                     str(self.ui.lineEdit_5.text()))
            conf.set('task', 'juexing',
                     str(self.ui.lineEdit_6.text()))
            conf.set('task', 'tupo',
                     str(self.ui.lineEdit_7.text()))

            # 御魂
            conf.set('mitama', 'mitama_click_partner_left',
                     'True')
            conf.set('mitama', 'mitama_click_partner_right',
                     'False')

            # 探索
            conf.set('explore', 'fight_boss_enable',
                     'True')
            conf.set('explore', 'tupo_enable',
                     'False')
    
    def get_conf(self, section):
        conf = configparser.ConfigParser()
        # 读取配置文件
        conf.read('conf.ini', encoding="utf-8")

        # 修改配置
        try:
            self.set_conf(conf, section)
        except:
            conf.add_section('watchdog')
            conf.add_section('explore')
            conf.add_section('mitama')
            conf.add_section('task')
            self.set_conf(conf, section)

        # 保存配置文件
        with open('conf.ini', 'w') as configfile:
                conf.write(configfile)

    def start_onmyoji(self):
        section = self.ui.tabWidget.currentIndex()

        # 读取配置
        self.get_conf(section)

        if section == 0:
            # 御魂
            if self.ui.mitama_single.isChecked():
                # 单刷
                self.fight = SingleFight()
    
            elif self.ui.mitama_driver.isChecked():
                # 司机
                self.fight = DriverFighter()
    
            elif self.ui.mitama_passenger.isChecked():
                # 乘客
                self.fight = FighterPassenger()

            elif self.ui.mitama_dual.isChecked():
                # 双开
                self.fight = DualFighter()
        
        elif section == 1:
            # 探索
            self.fight = ExploreFight()

        elif section == 2:
            # 百鬼夜行
            self.fight = Ghost()

        elif section == 3:
            # 结界突破
            if self.ui.individual.isChecked():
                # 个人突破
                self.fight = Breakthrough()

            elif self.ui.shack.isChecked():
                # 个人突破
                self.fight = ShackBreakthrough()

        elif section == 4:
            self.fight = Task()

        task = threading.Thread(target = self.fight.start)
        task.start()

    def stop_onmyoji(self):
        try:
            self.fight.deactivate()
        except:
            pass

if __name__=="__main__":  
    
    try:
        # 检测管理员权限
        if is_admin():
            global mode
            mode = 0
            global section
            section = 0

            # 设置战斗参数
            app = QApplication(sys.argv)
            myWin = MyMainWindow()
            myWin.show()
            sys.exit(app.exec_())

        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    except:
        pass
