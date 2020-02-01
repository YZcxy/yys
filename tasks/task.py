import configparser

from breakthrough.breakthrough import Breakthrough
from explore.explore import ExploreFight
from gameLib.fighter import Fighter
from mitama.single_fight import SingleFight


class Task(Fighter):

    def __init__(self):
        # 初始化
        Fighter.__init__(self, '专项任务')

        # 读取配置文件
        conf = configparser.ConfigParser()
        conf.read('conf.ini')
        self.tansuo = conf.getint('task', 'tansuo')
        self.yuhun = conf.getint('task', 'yuhun')
        self.juexing = conf.getint('task', 'juexing')
        self.tupo = conf.getint('task', 'tupo')

    def start(self):
        if self.run and self.tansuo > 0:
            self.switch_to_scene(4)
            tansuo = ExploreFight(max_tasks=self.tansuo, activate=False)
            tansuo.start()
        if self.run and self.yuhun > 0:
            self.switch_to_scene(7)
            yuhun = SingleFight(max_tasks=self.yuhun, activate=False)
            yuhun.start()
        if self.run and self.juexing > 0:
            self.switch_to_scene(6)
            juexing = SingleFight(max_tasks=self.juexing, activate=False)
            juexing.start()
        if self.run and self.tupo > 0:
            self.switch_to_scene(5)
            tupo = Breakthrough(max_tasks=self.tupo, activate=False)
            tupo.start()
