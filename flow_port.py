'''
Author: b1b2b3b4b5b6 a1439458305@163.com
Date: 2022-06-15 17:07:27
LastEditors: b1b2b3b4b5b6 a1439458305@163.com
LastEditTime: 2022-07-26 14:39:00
FilePath: \pyshow\flow_port.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''


import logging
import threading
from tkinter.tix import Tree
from urllib import request
import websocket
import jsonpickle
from queue import Queue


class Node:
    Normal = 'Normal'
    StandBy = 'StandBy'

    def __init__(self) -> None:
        self.name = ''
        self.xy = []
        self.typ = self.Normal
        self.nextNodeList = []

    def __str__(self) -> str:
        return jsonpickle.dumps(self, False)

    def __repr__(self) -> str:
        return self.__str__()


class Robot:
    def __init__(self, id: str, xy: list) -> None:
        self.id = id,
        self.xy = xy


class PonitConf:
    def __init__(self) -> None:
        self.nodeList = []
        self.groupDict = {}
        self.robotList = []


class FlowPort:
    def __init__(self, http_addr, websocket_addr) -> None:
        self.msg_queue = Queue()
        self.http_addr = http_addr
        self.websocket_addr = websocket_addr

    def Start(self):
        self.ws = websocket.WebSocketApp(
            self.websocket_addr, on_message=self.on_msg)
        t = threading.Thread(target=self.ws.run_forever)
        t.start()

    def on_msg(self, ws, msg):
        msg = jsonpickle.loads(msg)
        self.msg_queue.put(msg)

    def GetInitData(self) -> dict:
        jstr = request.urlopen(self.http_addr).read().decode()
        ret = jsonpickle.loads(jstr)
        return ret

    def GetPushData(self, time_s) -> dict:
        try:
            return self.msg_queue.get(timeout=time_s)
        except:
            return None

    def Stop(self):
        self.ws.close()
