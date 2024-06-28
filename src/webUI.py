from flask import Flask, render_template

app = Flask(__name__)

import pandas as pd

data = pd.read_csv('../res/raw_data - utf-8.csv', encoding='utf-8')
data.head()
movies = []
for item in data.values:
    movie = {}
    movie['时间'] = item[0]
    movie['标题'] = item[1]
    movie['访问量'] = item[2]
    movie['出处'] = item[3]
    movie['内容'] = item[4]
    movies.append(movie)
df = data.groupby('time').size()
times_keys = df.index.to_list()
times_values = df.values.tolist()
json_data = {}
json_data['keys'] = times_keys
json_data['values'] = times_values


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/movie')
def movie():
    return render_template('movie.html', movies=movies)


@app.route('/score')
def score():
    return render_template('score.html')


@app.route('/word')
def word():
    return render_template('word.html')


@app.route('/team')
def team():
    return render_template('team.html')


@app.route('/data')
def data():
    return json_data


@app.route('/chart')
def chart():
    return render_template('chart.html')


@app.after_request
def apply_caching(response):
    response.headers["Cache-Control"] = "no-cache"
    return response


if __name__ == '__main__':
    app.run(debug=True)
