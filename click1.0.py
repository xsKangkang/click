import pyautogui
import time
import random
import argparse
import logging
import json


# click
def click(x1=0, x2=0, y1=0, y2=0, init_run_time=0, num=0):
    for i in range(num): #  循环次数
        start = time.time()
        while True:
            run_time = time.time() - start
            if run_time > init_run_time:
                break
            print('No.'+str(i+1)+'  runtime: '+str(run_time))

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
        time.sleep(300) #  间隔5分钟


#  多窗口click
def click_(box, init_run_time=0, num=0):
    for i in range(num): #  循环次数
        start = time.time()
        while True:
            run_time = time.time() - start
            if run_time > init_run_time:
                break
            print('No.'+str(i+1)+'  runtime: '+str(run_time))

            time_keep_1 = random.uniform(0.5, 0.8)
            time_keep_2 = random.uniform(2, 3)
            for point in box:
                x = int(random.uniform(point[0], point[1]))   
                y = int(random.uniform(point[2], point[3]))
                ran = int(random.uniform(0, 2))
                if ran:
                    pyautogui.doubleClick(x, y)
                else:
                    pyautogui.click(x, y)
                time.sleep(time_keep_1)
            # pyautogui.doubleClick(1265, 626)
            time.sleep(time_keep_2)
        time.sleep(300) #  间隔5分钟


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


def logger(x1, x2, y1, y2, runtime, num, box):
    num_workers = 1
    if x1==0 and x2 == 0 and y1 == 0 and y2 == 0:
        num_workers = len(box)
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    sh = logging.StreamHandler()
    fmt = logging.Formatter("[%(asctime)s]-[%(levelname)s]-[%(filename)s]\nMessage:\n%(message)s")
    sh.setFormatter(fmt=fmt)
    log.addHandler(sh)
    if num_workers == 1:
        log.info(f'窗口数量为:1\n坐标为:{x1, y1}{x2, y2}\n运行时间为:{runtime}s\n循环次数:{num}')
    else:
        point = f'坐标为:'
        for i in box:
            x1, x2, y1, y2 = i
            point += f'\n{x1, y1}{x2, y2}'
        log.info(f'窗口数量为:{len(box)}\n' + point + f'\n运行时间为:{runtime}s\n循环次数:{num}')


def get_positon(num_workers):
    box = []
    print(f'窗口数量为:{num_workers}\n10s后开始录入坐标，按照提示鼠标移到目标点3秒不动即记录成功')
    time.sleep(10)
    for i in range(num_workers):
        print(f'开始录制第{i+1}个窗口:')
        time.sleep(0.5)
        x1, x2, y1, y2 = get_point()
        while not check_point(x1,x2,y1,y2):
            print('坐标错误，重新输入')
            x1, x2, y1, y2 = get_point()
        box.append([x1, x2, y1, y2])
    return box

def get_point():
    print('开始录制左上点：')
    time.sleep(1)
    x1, y1 = position()
    print('第一个点记录成功:{0},{1}'.format(x1, y1))
    time.sleep(1)
    print('开始录制右下点：')
    x2, y2 = position()
    print('第二个点记录成功:{0},{1}'.format(x2, y2))
    time.sleep(1)
    return(x1, x2, y1, y2)


def check_point(x1, x2, y1, y2):
    if (x1 > x2) or (y1 > y2):
        return False
    return True

def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_workers', type=int, default='1', help='number of workers')
    parser.add_argument('--classes', type=str, default='pata', help='')
    parser.add_argument('--time', type=int, default='3600', help='one hour')
    parser.add_argument('--option', type=str, default='option.json', help='path to json')
    parser.add_argument('--num', type=int, default=1, help='number')
    # parser.add_argument('--func', type=str, default='position', help='position or click')
    opt = parser.parse_args()
    return opt


def run():
    opt = parse_opt()
    runtime = opt.time
    classes = opt.classes
    option = opt.option
    num = opt.num
    num_workers = opt.num_workers

    if num_workers == 1:
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
                    x1, x2, y1, y2 = get_positon(num_workers)[0]
                    setting[classes] = {}
                    setting[classes]['position'] = [x1, x2, y1, y2]
                    setting[classes]['runtime'] = runtime
                    setting[classes]['label'] = classes
            with open(option, 'w') as f:
                json.dump(setting, f)
        else:
            x1, x2, y1, y2 = get_positon(num_workers)[0]
            opt_json = {classes: {}}
            opt_json[classes]['position'] = [x1, x2, y1, y2]
            opt_json[classes]['runtime'] = runtime
            opt_json[classes]['label'] = classes
            # path = f'{int(time.time())}option.json'
            path = f'option.json'
            with open(path, 'w') as f:
                json.dump(opt_json, f)
        logger(x1, x2, y1, y2, runtime,num, [])
        click(x1, x2, y1, y2, runtime, num)

    #  一次性使用多窗口
    else:
        box = get_positon(num_workers)
        logger(0, 0, 0, 0, runtime, num, box)
        click_(box, runtime, num)

if __name__ == '__main__':
    run()

# python click.py --classes pata --time 3600 --option option.json --num 3
'''
    --classes 后面跟类别,例如爬塔(pata)、魂土(huntu),可以使用多个配置(如果载入配置文件，不需要此项)
        默认值为pata,如果使用pata，则不需要此项
    --time 后面跟运行时间(单位是秒)(如果载入配置文件，不需要此项)
        默认值为3600(1h),如果使用3600,则不用此项
    --option 后跟配置文件,记录不同类别的信息(如果没有，则不需要此项，运行代码生成配置文件)
        默认值为空,如果一开始没有,则不用此项
    
    如果都不需要
    python click.py
'''
