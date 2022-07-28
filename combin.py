'''
Author: b1b2b3b4b5b6 a1439458305@163.com
Date: 2022-07-21 14:37:43
LastEditors: b1b2b3b4b5b6 a1439458305@163.com
LastEditTime: 2022-07-22 14:15:49
FilePath: \pyshow\combin.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import csv
from platform import node
import xml.etree.ElementTree as ET
import jsonpickle
from node import Node, PonitConf
import logging
from graph import graph

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s][%(levelname)s]%(filename)s[%(lineno)d]:  %(message)s', datefmt='%d/%b/%Y %H:%M:%S')


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


def read_csv(csv_file):
    r = csv.DictReader(open(csv_file), )
    ret = {}
    for d in r:
        ret[d['Point']] = Point(int(float(d['x']) * 1000),
                                int(float(d['y']) * 1000))
    return ret


def read_gexf(xml_file) -> ET.ElementTree:
    ET.register_namespace(
        '', "http://www.gexf.net/1.2draft")
    ET.register_namespace(
        'viz', "http://www.gexf.net/1.2draft/viz")
    ET.register_namespace(
        'xsi', "http://www.w3.org/2001/XMLSchema-instance")
    tree = ET.ElementTree(file=xml_file)
    return tree


def combine_gexf(tree: ET.ElementTree, d: dict, out_file):
    nodes = tree.find(
        '{http://www.gexf.net/1.2draft}graph').find('{http://www.gexf.net/1.2draft}nodes')
    for i in nodes.iter():
        name = i.get('id')
        if name is None:
            continue

        if name not in d.keys():
            print(name)
            exit(0)

        pos = i.find(r'{http://www.gexf.net/1.2draft/viz}position')
        point: Point = d[name]
        pos.set('x', str(point.x / 10))
        pos.set('y', str(-point.y / 10))
    tree.write(out_file, encoding='UTF-8', xml_declaration=True)


def combine_json(tree: ET.ElementTree, d: dict, out_file):
    node_dict = {}

    for k, v in d.items():
        v: Point = v
        n = Node()
        n.name = k
        n.xy = [v.x, v.y]
        if n.name[0] == 'S':
            n.typ = n.StandBy
        node_dict[n.name] = n

    edges = tree.find(
        '{http://www.gexf.net/1.2draft}graph').find('{http://www.gexf.net/1.2draft}edges')

    for i in edges.iter():
        name = i.get('id')
        start = i.get('source')
        end = i.get('target')

        if name is None:
            continue

        n: Node = node_dict[start]
        n.nextNodeList.append(end)
        n: Node = node_dict[end]
        n.nextNodeList.append(start)

    conf = PonitConf()
    conf.nodeList = list(node_dict.values())
    conf.groupDict = graph(node_dict).get_group()

    # group_dict = {}
    # print(group_dict)
    fp = open(out_file, 'w')
    fp.write(jsonpickle.dumps(conf, False))


combine_gexf(read_gexf('amr.gexf'), read_csv('xy.csv'), 'amr_out.gexf')
combine_json(read_gexf('amr.gexf'), read_csv('xy.csv'), 'amr_out.json')
