import pandas as pd
import numpy as np
from mongo_help import insert_comp, findone
from random import randint
import matplotlib.pyplot as plt

lis1 = []
lis2 = []

def get_mongo(data):
    s = findone({'_id': data})
    return s


def get(mongo_data, s_p=0, e_p=120):

    """
    mongo_data: 需要的数据
    s_p : 开始期号 (大于等于0)
    e_p : 结束期号（小于等于120）
    """
    i = 0
    s = mongo_data

    # a = np.random.randint(10, size=120)
    # b = np.random.randint(10, size=120)

    for li in s[gg][s_p:e_p]:
        n = li['num'][-3] # 每一期5个开奖号码中第4个号码
        n1 = li['num'][-1] # 每一期5个开奖号码中第5个号码
        lis1.append(int(n))
        lis2.append(int(n1))
        i += 1
    return e_p - s_p

def plot(k=120):
    """折线图"""

    plt.figure(figsize=[12.8, 9.6]) # figsize：指定图片大小
    plt.xlabel('issue') # 期号
    plt.ylabel('Winning numbers') # 中奖号码
    plt.title('plot')
    plt.plot(np.arange(k), lis1, label='fourth num')
    plt.plot(np.arange(k), lis2, label='fifth num')
    plt.legend()
    plt.show()


def scatter(k=120):
    """散点图"""
    plt.figure(figsize=[12.8, 9.6])
    plt.xlabel('issue') # 期号
    plt.ylabel('Winning numbers') # 中奖号码
    plt.title('scatter')
    plt.scatter(np.arange(k), lis1, label='fourth num')
    plt.scatter(np.arange(k), lis2, label='fifth num')
    plt.legend()
    plt.show()

def ws(k):
    """多个显示"""
    fig = plt.figure(figsize=[12.8, 9.6])
    fig.add_subplot(2, 2, 1)
    plt.xlabel('issue') # 期号
    plt.ylabel('Winning numbers') # 中奖号码
    # 直⽅图
    plt.hist(lis1, bins=10, color='r',edgecolor='black',label='fourth num') # edgecolor：边框颜色
    plt.legend()
    fig.add_subplot(2, 2, 2)
    # 散点图
    plt.scatter(np.arange(k), lis1, label='fourth num')
    plt.legend()
    plt.xlabel('issue') # 期号
    plt.ylabel('Winning numbers') # 中奖号码
    plt.title('scatter')
    fig.add_subplot(2, 2, 3)
    # 折线图
    plt.xlabel('issue') # 期号
    plt.ylabel('Winning numbers') # 中奖号码
    plt.plot(np.arange(k), lis1, label='fourth num')
    plt.legend()
    plt.show()

if __name__ == "__main__":

    gg = '20170111'
    d = get_mongo(gg)
    k = get(d)
    ws(k)
    # plot(k)
    # scatter(k)

    # b = [1,2,3]

    # print(b[-3:1])