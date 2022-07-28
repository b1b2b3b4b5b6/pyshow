
import csv
from ntpath import join


def read_csv(csv_file):
    r = csv.DictReader(open(csv_file), )
    ret = {}
    for d in r:
        ret[d['Point']] = {'x': d['x'], 'y': d['y']}
    return ret


def get_point(csv_data: dict, x, y):
    for k, v in csv_data.items():
        if v['x'] == x and v['y'] == y:
            return k
    return ''


def write_csv(csv_file, csv_data: dict):
    x_list = []
    y_list = []
    for k, v in csv_data.items():
        x_list.append(v['x'])
        y_list.append(v['y'])

    x_list = list(set(x_list))
    x_list.sort(key=lambda x: float(x))
    y_list = list(set(y_list))
    y_list.sort(key=lambda x: float(x), reverse=True)

    print(x_list)
    print(y_list)

    wl = ['']
    wl += x_list
    f = open(csv_file, 'w')
    f.write(','.join(wl) + '\n')
    for y in y_list:
        wl = [y]
        for x in x_list:
            wl.append(get_point(csv_data, x, y))
        f.write(','.join(wl) + '\n')

    f.close()


write_csv('out.csv', read_csv('xy.csv'))
