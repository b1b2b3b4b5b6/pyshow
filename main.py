'''
Author: your name
Date: 2022-03-31 02:49:59
LastEditTime: 2022-07-26 14:40:06
LastEditors: b1b2b3b4b5b6 a1439458305@163.com
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: \pyshow\main.py
'''

import json
import logging
from platform import node
from random import Random, randint, random
import threading
from time import sleep
from turtle import st
from urllib import request
from uuid import RESERVED_FUTURE
import pygame
from flow_port import FlowPort
import requests
logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s][%(levelname)s]%(filename)s[%(lineno)d]:  %(message)s', datefmt='%d/%b/%Y %H:%M:%S')


class Scalling:
    width = 1000
    height = 1000
    windows_scalling = [0.9, 0.9]
    minus_xy = [0, 0]
    scalling = [1, 1]

    def test_xy(node_dict: dict):
        x_list = []
        y_list = []
        for n in node_dict.values():
            n: Node = n
            x_list.append(n.xy[0])
            y_list.append(n.xy[1])
        min_xy = [min(x_list), min(y_list)]
        max_xy = [max(x_list), max(y_list)]

        Scalling.minus_xy = min_xy
        Scalling.scalling = [
            Scalling.width * Scalling.windows_scalling[0]/(max_xy[0] - min_xy[0]), Scalling.height * Scalling.windows_scalling[1]/(max_xy[1] - min_xy[1])]


class Node(object):
    Free = 'Free'
    Occupy = 'Occupy'
    Disable = 'Disable'
    Reserved = 'Reserved'

    Normal = 'Normal'
    StandBy = 'StandBy'

    def __init__(self, name, next_node_list, typ, xy) -> None:
        self.name = name
        self.xy = xy
        self.next_node_list = next_node_list
        self.status = self.Free
        self.typ = typ
        self.owner = None


class Robot(object):

    Removed = 'Removed'
    NotAssigned = 'NotAssigned'
    Enroute = 'Enroute'
    Parked = 'Parked'
    Acquiring = 'Acquiring'
    Depositing = 'Depositing'

    def __init__(self, id, xy=[0, 0]) -> None:
        self.id = id
        self.xy = xy
        self.status = self.Removed
        self.path = []


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
        temp = list(xy)
        temp = temp

        temp = list(map(lambda t: t[0]-t[1], zip(temp, Scalling.minus_xy)))
        temp = list(map(lambda t: int(t[0]*t[1]),
                        zip(temp, Scalling.scalling)))
        window_scalling = list(
            map(lambda t: (t[0]-t[1])/2, zip([1, 1], Scalling.windows_scalling)))
        window_left = list(map(lambda t:
                               int(t[0]*t[1]), zip([Scalling.width, Scalling.height], window_scalling)))

        temp = list(map(lambda t: int(
            t[0]+t[1]), zip(temp, window_left)))

        temp[1] = Scalling.height - temp[1]

        return temp


class ScreenMap(ScreenBase):
    def __init__(self, screen,  node_dict: dict, scaling: float = 1, name='default_map_screent',) -> None:
        super().__init__(screen, scaling, name)
        self.node_dict = node_dict
        pass

    def input(self, obj):
        pass

    def draw(self):
        surface = self.screen.convert_alpha()

        for k in self.node_dict.keys():
            start: Node = self.node_dict[k]

            for next in start.next_node_list:
                end: Node = self.node_dict[next]
                pygame.draw.line(surface, (233, 255, 255),
                                 self.trans_xy(start.xy), self.trans_xy(end.xy), 1)

        for k in self.node_dict.keys():
            start: Node = self.node_dict[k]

            if start.status == start.Free:
                color = (0, 255, 0)

            if start.status == start.Occupy:
                color = (0, 0, 255)

            if start.status == start.Reserved:
                color = (255, 255, 0)

            if start.status == start.Disable:
                color = (255, 0, 0)
            if start.typ == start.Normal:
                pygame.draw.circle(surface, color, self.trans_xy(start.xy), 7)
                pygame.draw.circle(surface, (0, 0, 0),
                                   self.trans_xy(start.xy), 7, 1)
            if start.typ == start.StandBy:
                pygame.draw.circle(surface, color, self.trans_xy(start.xy), 7)
                pygame.draw.circle(surface, (255, 255, 255),
                                   self.trans_xy(start.xy), 7, 1)

        GAME_FONT = pygame.freetype.Font(r"C:\Windows\Fonts\Consola.ttf", 13)
        for k in self.node_dict.keys():
            start: Node = self.node_dict[k]

            GAME_FONT.render_to(surface,  self.trans_xy(
                start.xy), f'  {k}', (0, 255, 255))

        self.screen.blit(surface, (0, 0))


class ScreenAMR(ScreenBase):
    def __init__(self, screen, amr_dict, node_dict, name='default_map_amr',) -> None:
        super().__init__(screen, name)
        self.amr_dict = amr_dict
        pass

    def input(self, obj):
        pass

    def draw(self):
        surface = self.screen.convert_alpha()

        GAME_FONT = pygame.freetype.Font(r"C:\Windows\Fonts\Consola.ttf", 15)
        for k in self.amr_dict.keys():
            v: Robot = self.amr_dict[k]

            # if v.status == v.READY:
            #     color = (0, 255, 0)

            # if v.status == v.MOVING:
            #     color = (0, 0, 255)

            # if v.status == v.PICKUP:
            #     color = (255, 0, 0)

            # if v.status == v.PICKUP:
            #     color = (255, 0, 0)

            color = (0, 255, 0)
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
                v.xy), f' {k}', (255, 0, 0))

            if len(v.path) > 0:
                start = xy
                end = self.trans_xy(node_dict[v.path[-1]].xy)
                pygame.draw.line(surface, (255, 0, 0), start, end, 2)

        self.screen.blit(surface, (0, 0))


def trans_obj(init_data: dict):

    node_dict = {}
    for d in init_data['nodeList']:
        n = Node(d['name'], d['nextNodeList'], d['typ'], d['xy'])
        node_dict[n.name] = n

    robot_dict = {}
    for d in init_data['robotList']:
        r = Robot(d['id'], d['initXy'])
        robot_dict[r.id] = r

    return node_dict, robot_dict


my = FlowPort('http://127.0.0.1:5006/api/Map/GetInitData',
              'ws://127.0.0.1:14399')
my.Start()
node_dict, robot_dict = trans_obj(my.GetInitData())
Scalling.test_xy(node_dict)

pygame.init()
screen = pygame.display.set_mode((Scalling.width, Scalling.height))
screen.fill((119, 136, 153))
print(screen.get_size())

pygame.display.set_caption("amr展示")

screen_map = ScreenMap(screen, node_dict)
screen_amr = ScreenAMR(screen, robot_dict, node_dict)
screen_amr.draw()
screen_map.draw()


def assign():
    def get_random_node():
        ret = []
        for n in node_dict.values():
            n: Node = n
            if n.typ == n.StandBy:
                continue
            if n.status == n.Disable:
                continue
            ret.append(n.name)
        return ret[randint(0, len(ret) - 1)]
    while True:
        sleep(1)
        for r in robot_dict.values():
            r: Robot = r
            if r.status == r.NotAssigned:
                d = {}
                d['deviceId'] = r.id
                d['pathList'] = [get_random_node()]
                logging.info(d)
                ret = requests.post(
                    'http://127.0.0.1:5006/api/Mission/ManualAssignMove', json=d)


t = threading.Thread(target=assign)
t.start()

while True:
    data = my.GetPushData(0)
    if data is not None:
        if data['typ'] == 'RobotInfo':
            r: Robot = robot_dict[data['id']]
            r.xy = data['xy']
            r.status = data['status']
            r.path = data['path']

        if data['typ'] == 'MapInfo':
            for n in node_dict.values():
                n: Node = n
                n.status = n.Free
                n.owner = None
            for d in data['nodeList']:
                n = node_dict[d['name']]
                if d['status'] == 'Free':
                    n.status = n.Free
                if d['status'] == 'Occupy':
                    n.status = n.Occupy
                if d['status'] == 'Reserved':
                    n.status = n.Reserved
                if d['attribute'] == 'Disable':
                    n.status = n.Disable
                n.owner = d['ownerDevice']

    screen.fill((119, 136, 153))
    screen_amr.draw()
    screen_map.draw()
    pygame.display.flip()  # 更新屏幕内容

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            my.Stop()
            exit(0)
