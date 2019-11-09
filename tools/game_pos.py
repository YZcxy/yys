class GamePos():
    def __init__(self,pos,pos_end=None):
        self.pos=pos
        self.pos_end=pos_end

class CommonPos():
    first_position = (30, 80),(200, 452)
    second_position = (940, 80), (1111, 452)  # 第二次结算所点击的位置

class TansuoPos():
    last_chapter = (934, 493), (1108, 572)  # 列表最后一章
    tansuo_btn=(787,458),(890,500) #探索按钮
    tansuo_denglong = (424, 118), (462, 158)  # 探索灯笼
    ready_btn = (1000, 460), (1069, 513)  # 准备按钮
    fight_quit=GamePos((1055,462),(1121,518)) #退出战斗
    quit_btn = (32, 45), (58, 64)  # 退出副本
    confirm_btn = (636, 350), (739, 370)  # 退出确认按钮
    change_monster = (427, 419), (457, 452)  # 切换狗粮点击区域
    quanbu_btn = (37, 574), (80, 604)  # “全部”按钮
    n_tab_btn = (142, 288), (164, 312)  # n卡标签
    n_slide = (168, 615), (784, 615)  # n卡进度条，从头至尾
    quit_change_monster=GamePos((19,17),(43,38)) #退出换狗粮界面
    gouliang_middle = (397, 218), (500, 349)  # 中间狗粮位置
    gouliang_right = (628, 293), (730, 430)  # 右边狗粮位置

class YuhunPos():
    tiaozhan_btn = (790, 418), (903, 469)    # 御魂挑战按钮
    kaishizhandou_btn = (1048, 535), (1113, 604)   # 御魂开始战斗按钮

class GhostPos():
    jinru_btn = (770, 450), (875, 485)   # 进入百鬼夜行按钮
    king_position = (((200, 330),(280, 470)),((530, 330),(610, 470)),((820, 330),(900, 470)))   # 三组鬼王的位置
    start_btn = (1000, 500), (1090, 590)  # 开始砸百鬼按钮
    ghost_position = (70, 300), (1050, 480)  # 百鬼的大致位置
    jiesuan_position = (60, 80),(150, 550)  # 百鬼契约书位置
    beans_position = (340, 590) # 百鬼初始豆子中心位置