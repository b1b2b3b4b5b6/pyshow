'''
Author: b1b2b3b4b5b6 a1439458305@163.com
Date: 2022-07-20 15:05:31
LastEditors: b1b2b3b4b5b6 a1439458305@163.com
LastEditTime: 2022-07-22 13:06:09
FilePath: \pyshow\generate_json.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''

import json
import jsonpickle


class Node:
    Normal = 'Normal'
    StandBy = 'StandBy'

    def __init__(self) -> None:
        self.name = ''
        self.xy = []
        self.typ = self.Normal
        self.radius = 10
        self.nextNodeList = []

    def __str__(self) -> str:
        return jsonpickle.dumps(self, False)

    def __repr__(self) -> str:
        return self.__str__()


class PonitConf:
    def __init__(self) -> None:
        self.nodeList = []
        self.groupDict = {}
