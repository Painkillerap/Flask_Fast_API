from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
@app.route('/main/')
def main_page():
    context = {'title': 'Интернет-магазин: Главная'}
    return render_template('main.html', **context)

@app.route('/clothes/')
def clothes_page():
    context = {'title': 'Интернет-магазин: Одежда'}
    return render_template('clothes.html', **context)


@app.route('/footwear/')
def footwear_page():
    context = {'title': 'Интернет-магазин: Обувь'}
    return render_template('footwear.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
