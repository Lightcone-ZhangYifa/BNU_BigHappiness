import pandas as pd
from collections import Counter
import jieba.posseg as pseg
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# 饼图&词云图
plt.rcParams['font.size'] = 37
plt.rcParams['text.usetex'] = False
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['font.family'] = "SimHei"
dafu = pd.read_csv('../res/raw_data - utf-8.csv', encoding='utf-8')
years = list(map(int, set(dafu['time'].str[:4].tolist())))
years.sort()

dafu['time'] = pd.to_datetime(dafu['time'])
groups = dafu.groupby(dafu['time'].dt.year)
print(groups)
wc = WordCloud(font_path="C:\Windows\Fonts\simsun.ttc", background_color="white", width=1200, height=700)


def title_to_nouns_number(li_: list) -> dict:
    str_ = ' '.join(li_)
    words = pseg.cut(str_)
    nouns = [word for word, flag in words if flag == 'n' and len(word) >= 2]
    counter = Counter(nouns)
    return counter


for i in range(len(years)):
    li_ = groups.get_group(years[i])['title'].tolist()
    data = title_to_nouns_number(li_)
    data_keys = list(data.keys())
    data_values = list(data.values())
    plt.figure(figsize=(25, 25))
    plt.pie(data_values[:15], labels=data_keys[:15], autopct='%1.1f%%')
    plt.title(f'{years[i]}年名词出现频率', fontproperties="SimHei")
    plt.savefig(f'static/assets/img/饼图{years[i]}.png', dpi=350)
    plt.show()
    plt.figure(figsize=(20, 16))
    wc.fit_words(data)
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(f'static/assets/img/词云图{years[i]}.png', dpi=300)
    plt.show()
