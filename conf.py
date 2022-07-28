def read_csv(csv_file):
    ret = {}
    r = csv.DictReader(open(csv_file))
    for d in r:
        y = d.pop('xy')
        for k, v in d.items():
            x = k
            if v != '':
                ret[v] = {'x': x, 'y': y}
    return ret


def get_nodeList(data: dict):
    ret = []
    for k, v in data.items():
        n = node()
        n.name = k
        n.xy = [float(v['x']), float(v['y'])]
        if n.name[0] == 'S':
            n.typ = n.StandBy
        ret.append(n)
    return ret


def generate_line(nl: list):
    x_list = []
    y_list = []

    for n in nl:
        n: node = n
        if n.xy[0] < 0:
            x_list.append(n.xy[0])
        if n.xy[1] < 0:
            y_list.append(n.xy[1])
    x_list = list(set(x_list))
    y_list = list(set(y_list))
    print(x_list)
    print(y_list)


d = read_csv('final.csv')
nl = get_nodeList(d)
generate_line(nl)
