'''
Author: your name
Date: 2022-03-31 02:49:59
LastEditTime: 2022-04-01 00:25:05
LastEditors: Please set LastEditors
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: \pyshow\main.py
'''

import logging
import matplotlib.pyplot as plt
import pygame
import networkx as nx

import csv


logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s][%(levelname)s]%(filename)s[%(lineno)d]:  %(message)s', datefmt='%d/%b/%Y %H:%M:%S')


class Side(object):
    def __init__(self, start_xy=0, end_xy=0) -> None:
        self.start_xy = start_xy
        self.end_xy = end_xy
        self.length = self.get_distance(start_xy, end_xy)

    def get_distance(self, f_xy, t_xy):

        dis = ((t_xy[0] - f_xy[0])**2 + (t_xy[1] - f_xy[1])**2)**0.5

        return round(dis, 2)


class Point(object):
    FREE = 'free'
    OCCUPY = 'OCCUPY'
    DISABLED = 'DISABLED'

    def __init__(self, name: str, xy: list) -> None:
        self.name = name
        self.xy = list(xy)
        self.next_reach_dict = {}
        self.status = self.FREE
        self.owner = None


class PointMap(object):

    def __init__(self, point_dict: dict, name='default_point_map') -> None:
        self.name = name
        self.raw_dict = point_dict

    def __str__(self) -> str:
        return f'map[{self.name}]'

    def connenct_check(self) -> bool:
        if len(self.raw_dict) == 0:
            logging.error(f'{self.name} has no point')
            return False

        first_point: Point = self.raw_dict[self.raw_dict.keys[0]]
        walked_list = []

        def dp(p: Point):
            if p in walked_list:
                return

            d = p.next_reach_dict
            if len(d) == 0:
                logging.error(f'{self.name} ')
                return False
            for k in d.keys():
                dp(self.raw_dict[k])

        dp(first_point)
        if len(walked_list) != len(self.raw_dict):
            logging.error(f'{self} can not full connect')
            return False

        return True

    def custom_check(self) -> bool:
        return True

    def show_net(self) -> None:
        G = nx.DiGraph()

        for k in self.raw_dict.keys():
            p: Point = self.raw_dict[k]
            if p.status == p.DISABLED:
                continue

            for n in p.next_reach_dict.keys():
                G.add_edge(
                    k, n, weight=p.next_reach_dict[n].length)

        # print(nx.is_connected(G))
        if(nx.number_strongly_connected_components(G) != 1):
            logging.error(f'{self} is not strong connect')

        weights = nx.get_edge_attributes(G, "weight")
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, edge_color='b',
                node_color='g', node_size=1000)
        nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=weights)

        plt.show()


class AMR(object):
    READY = 'ready'
    PICKUP = 'pickup'
    DROPDWON = 'dropdown'
    MOVING = 'moving'

    def __init__(self, name, xy=[0, 0]) -> None:
        self.name = name
        self.status = self.READY
        self.xy = xy


def read_csv() -> PointMap:
    fp = open('xy.csv', encoding='utf-8')
    raw_list = list(csv.DictReader(fp))
    xy_dict = {}
    for l in raw_list:
        xy_dict[l['Point']] = [float(l['x']), float(l['y'])]

    fp = open('connection.csv', encoding='utf-8')
    raw_list = list(csv.DictReader(fp))
    connect_dict = {}
    for l in raw_list:
        now_point = l.pop(r'From\To')
        connect_dict[now_point] = {}
        now_dict = connect_dict[now_point]
        for k in l.keys():
            num = float(l[k])
            if num != 0:
                now_dict[k] = num

    point_dict = {}
    for k in xy_dict.keys():
        p = Point(k, list(xy_dict[k]))
        point_dict[k] = p
        con: dict = connect_dict[k]
        for n in con.keys():
            p.next_reach_dict[n] = Side(xy_dict[k], xy_dict[n])

    pm = PointMap(point_dict)
    # pm.show_net()
    return pm


class ScreenBase(object):
    def __init__(self, screen, scaling: float = 1, name='default_screen') -> None:
        self.name = name
        self.screen = screen
        self.scaling = scaling
        pass

    def input(self, obj):
        pass

    def draw(self):
        pass

    def trans_xy(self, xy) -> list:
        return [int(xy[0] * self.scaling)+30, self.screen.get_size()[1] - (int(xy[1]*self.scaling)+250)]


class ScreenMap(ScreenBase):
    def __init__(self, screen,  pm: PointMap, scaling: float = 1, name='default_map_screent',) -> None:
        super().__init__(screen, scaling, name)
        self.pm = pm
        pass

    def input(self, obj):
        pass

    def draw(self):
        surface = self.screen.convert_alpha()

        for k in self.pm.raw_dict.keys():
            p: Point = self.pm.raw_dict[k]

            for t in p.next_reach_dict.keys():
                l: Side = p.next_reach_dict[t]
                pygame.draw.line(surface, (233, 255, 255),
                                 self.trans_xy(l.start_xy), self.trans_xy(l.end_xy), 1)

        for k in self.pm.raw_dict.keys():
            p: Point = self.pm.raw_dict[k]

            if p.status == p.FREE:
                color = (0, 255, 0)

            if p.status == p.OCCUPY:
                color = (0, 0, 255)

            if p.status == p.OCCUPY:
                color = (255, 0, 0)
            pygame.draw.circle(surface, color, self.trans_xy(p.xy), 7)
            pygame.draw.circle(surface, (0, 0, 0), self.trans_xy(p.xy), 7, 1)

        GAME_FONT = pygame.freetype.Font(r"C:\Windows\Fonts\Consola.ttf", 15)
        for k in self.pm.raw_dict.keys():
            p: Point = self.pm.raw_dict[k]

            GAME_FONT.render_to(surface,  self.trans_xy(
                p.xy), f'  {k}', (0, 255, 255))

        self.screen.blit(surface, (0, 0))


class ScreenAMR(ScreenBase):
    def __init__(self, screen, scaling: float = 1, name='default_map_amr',) -> None:
        super().__init__(screen, scaling, name)
        self.amr_dict = {}
        self.amr_dict['1'] = AMR('1', [4.5, 1.06])
        self.amr_dict['2'] = AMR('2', [10.31, 11.38])

        pass

    def input(self, obj):
        pass

    def draw(self):
        surface = self.screen.convert_alpha()

        GAME_FONT = pygame.freetype.Font(r"C:\Windows\Fonts\Consola.ttf", 15)
        for k in self.amr_dict.keys():
            v: AMR = self.amr_dict[k]

            if v.status == v.READY:
                color = (0, 255, 0)

            if v.status == v.MOVING:
                color = (0, 0, 255)

            if v.status == v.PICKUP:
                color = (255, 0, 0)

            if v.status == v.PICKUP:
                color = (255, 0, 0)

            xy = self.trans_xy(v.xy)
            temp = 7
            w = 4

            pygame.draw.line(surface, color, xy, [
                             xy[0] + temp, xy[1] + temp], w)
            pygame.draw.line(surface, color, xy, [
                             xy[0] + temp, xy[1] - temp], w)
            pygame.draw.line(surface, color, xy, [
                             xy[0] - temp, xy[1] - temp], w)
            pygame.draw.line(surface, color, xy, [
                             xy[0] - temp, xy[1] + temp], w)
            pygame.draw.circle(surface, (0, 0, 0),
                               self.trans_xy(v.xy), 2)
            # pygame.draw.circle(surface, (0, 0, 0),
            #                    self.trans_xy(v.xy), 6)
            # pygame.draw.circle(surface, color, self.trans_xy(v.xy), 3)

            GAME_FONT.render_to(surface,  self.trans_xy(
                v.xy), f' {k}', (255, 215, 0))

        self.screen.blit(surface, (0, 0))


pygame.init()
screen = pygame.display.set_mode((1000, 1000))
screen.fill((119, 136, 153))
print(screen.get_size())

pygame.display.set_caption("amr展示")

screen_map = ScreenMap(screen, read_csv(), scaling=35)
screen_map.draw()

screen_amr = ScreenAMR(screen, scaling=35)
screen_amr.draw()
while True:
    pygame.display.flip()  # 更新屏幕内容
    # mouse_pos = pygame.mouse.get_pos()
    # # 设置事件触发类型
    # MY_EVENT = pygame.USEREVENT + 1
    # # 设置事件触发条件：鼠标移动到指定区域
    # if 225 < mouse_pos[0] < 375 and 150 < mouse_pos[1] < 250:
    #     # 增加一个事件
    #     my_event = pygame.event.Event(MY_EVENT, {"message": "事件触发"})
    #     # 将这个事件加入到事件队列
    #     pygame.event.post(my_event)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
