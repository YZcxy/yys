class GamePos():
    def __init__(self,pos,pos_end=None):
        self.pos=pos
        self.pos_end=pos_end

class CommonPos():
    first_position = (30, 80),(200, 452)
    second_position = (940, 80), (1111, 452)  # 第二次结算所点击的位置
    left_partner_position = (90, 393), (208, 517) # 最左边的式神位置
    right_partner_position = (895, 380), (975, 488) # 最右边的式神位置

class TansuoPos():
    last_chapter = (934, 493), (1108, 572)  # 列表最后一章
    tansuo_btn=(787,458),(890,500) #探索按钮
    tansuo_denglong = (424, 118), (462, 158)  # 探索灯笼
    jiejie_tupo = (255, 570), (295, 605) # 探索页面下方的结界突破按钮
    juexing_cailiao = (65, 570), (108, 605)  # 探索页面下方的觉醒材料按钮
    leiqilin = (900, 120), (1040, 520)  # 雷麒麟
    yuhun = (160, 570), (210, 605)  # 探索页面下方的御魂按钮
    baqidashe = (160, 130), (335, 420)  # 八岐大蛇
    quit_zhangjie_btn = (919, 119), (947, 145) # 退出章节页面的小叉叉
    quit_tupo_btn = (1040, 50), (1065, 75)  # 退出结界突破页面的小叉叉
    tupo_tickets = (822, 10), (915, 40) # 章节页面，突破门票的数量位置
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
    tiaozhan_btn = (1000, 540), (1053, 596)    # 御魂挑战按钮
    kaishizhandou_btn = (1048, 535), (1113, 604)   # 御魂开始战斗按钮

class GhostPos():
    jinru_btn = (770, 450), (875, 485)   # 进入百鬼夜行按钮
    king_position = (((200, 330),(280, 470)),
                     ((530, 330),(610, 470)),
                     ((820, 330),(900, 470)))   # 三组鬼王的位置
    start_btn = (1000, 500), (1090, 590)  # 开始砸百鬼按钮
    ghost_position = (70, 300), (1050, 480)  # 百鬼的大致位置
    jiesuan_position = (60, 80),(150, 550)  # 百鬼契约书位置
    beans_position = (340, 590) # 百鬼初始豆子中心位置

class BreakthroughPos():
    # 结界突破位置
    target_position = (((117, 80), (410, 195)),
                       ((422, 80), (718, 195)),
                       ((728, 80), (1023, 195)),
                       ((117, 202), (410, 315)),
                       ((422, 202), (718, 315)),
                       ((728, 202), (1023, 315)),
                       ((117, 322), (410, 434)),
                       ((422, 322), (718, 434)),
                       ((728, 322), (1023, 434)))  # 六组突破目标位置
    refresh_position = ((858, 458), (1007, 503)) # 刷新按钮位置
    confirm_btn = ((600, 362), (750, 408)) # 确认刷新按钮
    jiesuan_position = (90, 20), (425, 70)  # 结算位置，防止误点，范围很小
    # 寮突破位置
    shack_target_position = (((365, 95), (660, 207)),
                            ((665, 95), (960, 207)),
                            ((365, 215), (660, 327)),
                            ((665, 215), (960, 327)),
                            ((365, 335), (660, 447)),
                            ((665, 335), (960, 447)),
                            ((365, 455), (660, 567)),
                            ((665, 455), (960, 567)))    # 八组突破目标位置

    quit_btn = (22, 20), (42, 40)  # 退出战斗
    confirm_quit_btn = (615, 363), (702, 386)  # 退出确认按钮
