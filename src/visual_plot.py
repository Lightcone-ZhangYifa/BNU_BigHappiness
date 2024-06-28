# 按月份的折线图
import pandas as pd
from collections import Counter
import jieba.posseg as pseg
import matplotlib.pyplot as plt

plt.rcParams['font.size'] = 30
plt.rcParams['text.usetex'] = False
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['font.family'] = "SimHei"
plt.figure(figsize=(30, 15))
plt.title('折线图', fontproperties="SimHei")
plt.xlabel('日期', fontproperties="SimHei")
plt.ylabel('词频', fontproperties="SimHei")
dafu = pd.read_csv('../res/raw_data - utf-8.csv', encoding='utf-8')
times = list(map(str, set(dafu['time'].str[:7].tolist())))
times = list(set(times))
times.sort()


def title_to_nouns_number(li_: list) -> dict:
    str_ = ' '.join(li_)
    words = pseg.cut(str_)
    nouns = [word for word, flag in words if flag == 'n' and len(word) >= 3]
    counter = Counter(nouns)
    return counter


my_dict = title_to_nouns_number(dafu['title'].tolist())
sorted_dict = dict(sorted(my_dict.items(), key=lambda item: item[1], reverse=True))
# print(len(sorted_dict))
# 取前五个词
sorted_dict_keys = list(sorted_dict.keys())[:5]

sorted_dict_values = []
for key in sorted_dict_keys:
    value = []
    for i in range(len(times)):
        mask = dafu['time'].str.contains(times[i], case=False)
        x1 = dafu[mask].index[0]
        x2 = dafu[mask].last_valid_index()
        counts = title_to_nouns_number(dafu['title'][x1:x2 + 1])
        value.append(counts[key])
    sorted_dict_values.append(value)

# 最后画图
for i in range(5):
    plt.plot(times, sorted_dict_values[i], label=sorted_dict_keys[i])
    plt.legend()

# 显示图表
plt.savefig('static/assets/img/折线图.png', dpi=350)
plt.show()
