import pyautogui
import time
import random
import argparse
import logging
import json


# click
def click(x1, x2, y1, y2, init_run_time):
    start = time.time()
    while True:
        run_time = time.time() - start
        if run_time > init_run_time:
            break
        print('runtime: '+str(run_time))

        time_keep = random.uniform(2, 3)
        x = int(random.uniform(x1, x2))
        y = int(random.uniform(y1, y2))
        ran = int(random.uniform(0, 2))
        if ran:
            pyautogui.doubleClick(x, y)
        else:
            pyautogui.click(x, y)
        # pyautogui.doubleClick(1265, 626)

        time.sleep(time_keep)


# position
def position():
    time_start = time.time()
    x0, y0 = pyautogui.position()
    while True:
        time_end = time.time()
        if time_end - time_start > 3:
            return pyautogui.position()
        x, y = pyautogui.position()
        if (x != x0) or (y != y0):
            x0 = x
            y0 = y
            time_start = time_end
            print('no move')
        time.sleep(0.5)


def logger(x1, x2, y1, y2, runtime):
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    sh = logging.StreamHandler()
    fmt = logging.Formatter("[%(asctime)s]-[%(levelname)s]-[%(filename)s]\nMessage:\n%(message)s")
    sh.setFormatter(fmt=fmt)
    log.addHandler(sh)
    log.info(f'坐标为:{x1, y1}{x2, y2}\n运行时间为:{runtime}s')


def get_positon():
    print('10s后开始录入坐标，按照提示鼠标移到目标点3秒不动即记录成功')
    time.sleep(10)
    print('开始录制左上点：')
    time.sleep(1)
    x1, y1 = position()
    print('第一个点记录成功:{0},{1}'.format(x1, y1))
    time.sleep(1)
    print('开始录制右下点：')
    x2, y2 = position()
    print('第二个点记录成功:{0},{1}'.format(x2, y2))
    time.sleep(1)
    return x1, x2, y1, y2


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--classes', type=str, default='pata', help='')
    parser.add_argument('--time', type=int, default='', help='one hour')
    parser.add_argument('--option', type=str, default='', help='path to json')
    # parser.add_argument('--func', type=str, default='position', help='position or click')
    opt = parser.parse_args()
    return opt


def run():
    opt = parse_opt()
    runtime = opt.time
    classes = opt.classes
    option = opt.option

    if option != '':
        with open(option) as f:
            setting = json.load(f)
            if classes in setting.keys():
                if runtime:
                    setting[classes]['runtime'] = runtime
                else:
                    runtime = setting[classes]['runtime']
                x1, x2, y1, y2 = setting[classes]['position']
                
            else:
                x1, x2, y1, y2 = get_positon()
                setting[classes] = {}
                setting[classes]['position'] = [x1, x2, y1, y2]
                setting[classes]['runtime'] = runtime
                setting[classes]['label'] = classes
        with open(option, 'w') as f:
            json.dump(setting, f)
    else:
        x1, x2, y1, y2 = get_positon()
        opt_json = {classes: {}}
        opt_json[classes]['position'] = [x1, x2, y1, y2]
        opt_json[classes]['runtime'] = runtime
        opt_json[classes]['label'] = classes
        # path = f'{int(time.time())}option.json'
        path = f'option.json'
        with open(path, 'w') as f:
            json.dump(opt_json, f)
    logger(x1, x2, y1, y2, runtime)
    click(x1, x2, y1, y2, runtime)


if __name__ == '__main__':
    print('begin')
    run()

# python click.py --classes pata --time 3600 --option option.json
'''
    --classes 后面跟类别,例如爬塔(pata)、魂土(huntu)
        默认值为pata,如果使用pata，则不需要此项
    --time 后面跟运行时间(单位是秒)

    --option 后跟配置文件,记录不同类别的信息(如果没有，则不需要此项，运行代码生成配置文件)
        默认值为空,如果一开始没有,则不用此项
    
'''
