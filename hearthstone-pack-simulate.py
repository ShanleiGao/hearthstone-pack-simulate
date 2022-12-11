import pandas as pd
import numpy as np
import matplotlib
import random

NORMAL, RARE, EPIC, LEGEND = 0, 1, 2, 3
BREAK = [5,20,100,400] #分解可得奥术之尘
MAKE = [40,100,400,1600] #用奥术之尘合成
RATE = [1,0.25,0.05,0.01] #各稀有度累计概率

def open(target):
    total = [0,0,0,0] #总张数
    dust = 0 #奥术之尘数量
    dustRemains = sum((target[i] * MAKE[i]) for i in range(4)) #合成所有未拥有的卡所需奥术之尘
    legendCnt = 0 #连续不出橙的包数
    result = 0 #所开卡包计数
    while dust < dustRemains:
        pack = [0,0,0,0] #当前包各稀有度张数

        #当连续40包不出橙时，强制出一张橙
        if legendCnt == 40:
            pack[LEGEND] += 1
            legendCnt = 0

        #Roll该包中的每一张
        for _ in range(4 if pack[LEGEND] else 5):
            curr = random.random()
            if curr < RATE[LEGEND]:
                pack[LEGEND] += 1
                legendCnt = 0
            elif curr < RATE[EPIC]:
                pack[EPIC] += 1
            elif curr < RATE[RARE]:
                pack[RARE] += 1
            else:
                pack[NORMAL] += 1

        #如果该包中全为白卡，将其中的一张转换为蓝卡
        if pack[NORMAL] == 5:
            pack[NORMAL] -= 1
            pack[RARE] += 1

        #用当前包的情况进行更新
        for i in range(4):
            new = min(pack[i], target[i] - total[i]) #所获新牌数量
            old = pack[i] - new #所获旧牌数量
            dust += old * BREAK[i] #将旧牌分解为奥术之尘
            total[i] += new #将新牌加入收藏
            dustRemains -= new * MAKE[i] #加入收藏后，减少合成未拥有卡牌所需要的奥术之尘数量

        #如果当前包未出橙，更新连续未出橙数量
        if pack[LEGEND] == 0:
            legendCnt += 1

        result += 1
        
    return result

#每个扩展包，各稀有度的总张数分别为 50, 35, 25, 24
results = []
for _ in range(1000000):
    results.append(open([100, 70, 50, 24]))

print(np.mean(results), np.std(results))

df = pd.DataFrame({'Packs':results})
df.plot(kind='hist', grid=True, legend=False, figsize=(10,8),bins=100)