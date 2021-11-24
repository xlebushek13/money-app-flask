from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random

app = Flask(__name__)
app.config["MYSQL_HOST"] = "roombox.mysql.tools"
app.config["MYSQL_USER"] = "roombox_moneyapp"
app.config["MYSQL_PASSWORD"] = "01112003bK"
app.config["MYSQL_DB"] = "roombox_moneyapp"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql+pymysql://roombox_moneyapp:01112003bK@roombox.mysql.tools/roombox_moneyapp"

db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return "<Article %r>" % self.id


@app.route("/")
@app.route("/home")
def home():
    afforizm_array = [
        "Если деньги не жалеют людей, то почему люди должны жалеть деньги?!",
        "Никогда не трать деньги с умом. Деньги к тебе ещё вернутся, а вот ум…",
        "Деньги не имеют значения — пока они у вас есть.",
        "Если ваше счастье не в деньгах, то шлите их мне.",
        "Счастье не в деньгах, а в деньжищах.",
        "Всех денег не заработать — часть придется украсть.",
        "Если время – деньги, значит, наше время ещё не пришло.",
        "Кредит — это когда денег не то чтобы совсем нет, а ещё меньше.",
        "Деньги — лучшее успокоительное средство.",
        "Если каждый месяц откладывать понемногу, то уже через год вы будете удивлены, как мало у вас набралось.",
        "Считать деньги в чужом кармане нехорошо, но интересно.",
        "Пусть деньги зло, но с ними я добрею.",
        "Если деньги не радуют — значит, они не ваши.",
        "Копить деньги — вещь полезная, особенно если это сделали за вас родители.",
        "Чтобы стать богатым, необходимо три вещи: ум, талант и много денег.",
        "Жизнь — игра, а деньги — способ вести счет.",
        "Деньги портят человека, когда они у других.",
        "Лопатой деньги гребут те, кто лопату в руках не держал.",
        "Деньги — это грязь, но лечебная.",
        "Экономия — способ тратить деньги без удовольствия.",
        "Вы никогда не заработаете денег, если все еще думаете, что их зарабатывают…",
        "Время течет, деньги чаще всего утекают, а от некоторых – улепетывают!",
        "Если человек говорит, что деньги могут все, значит, у него нет ни гроша.",
        "Если ваш бухгалтер платит все налоги, пусть получает зарплату в налоговой инспекции.",
        "Деньги, они как дети — пока маленькие, то и запросы маленькие.",
        "Дача денег в долг тренирует память.",
        "Излишняя полнота к лицу только кошельку.",
        "Кто хочет разбогатеть в течение дня, будет повешен в течение года.",
        "Деньги — зло, а добро — это то, что мы на эти деньги покупаем.",
        "Деньги не пахнут – пахнут только большие деньги. Изумительный аромат!",
    ]
    now = afforizm_array[random.randint(0, 29)]
    return render_template("index.html", afforizm_array=now)


@app.route("/statistic")
def statistic():
    articles = Article.query.order_by(Article.date.asc()).all()
    statistic_dict = {}
    statistic_title_array = []
    statistic_date_array = []
    statistic_price_array = []

    for i in articles:
        if i.title not in statistic_dict:
            statistic_dict[i.title] = i.price
        elif i.title in statistic_dict:
            statistic_dict[i.title] = statistic_dict.get(i.title) + i.price

    for i in articles:
        statistic_title_array.append(
            str(i.title) + ": " + str(i.date.day) + " " + str(i.date.month)
        )
        statistic_date_array.append(str(i.date.day) + " " + str(i.date.month))
        statistic_price_array.append(i.price)

    legend = "Цена"
    title = statistic_title_array
    labels = statistic_date_array
    values = statistic_price_array

    return render_template(
        "statistic.html",
        statistic_dict=statistic_dict,
        values=values,
        labels=labels,
        legend=legend,
        title=title,
    )


@app.route("/statistic-month")
def statistic_month():
    time = datetime.utcnow()
    year = str(time.year)
    month = str(time.month)
    if month != "10" or "11" or "12":
        month = "0" + month

    articles = (
        Article.query.filter(Article.date.startswith(year + "-" + month))
        .order_by(Article.date.asc())
        .all()
    )
    statistic_dict = {}
    statistic_date_array = []
    statistic_price_array = []
    statistic_title_array = []

    for i in articles:
        if i.title not in statistic_dict:
            statistic_dict[i.title] = i.price
        elif i.title in statistic_dict:
            statistic_dict[i.title] = statistic_dict.get(i.title) + i.price

    for i in articles:
        statistic_title_array.append(
            str(i.title) + ": " + str(i.date.day) + " " + str(i.date.month)
        )
        statistic_date_array.append(str(i.date.day) + " " + str(i.date.month))
        statistic_price_array.append(i.price)

    legend = "Цена"
    title = statistic_title_array
    labels = statistic_date_array
    values = statistic_price_array

    return render_template(
        "statistic-month.html",
        statistic_dict=statistic_dict,
        values=values,
        labels=labels,
        legend=legend,
        title=title,
    )


@app.route("/posts")
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articles=articles)


@app.route("/posts/<int:id>")
def posts_detail(id):
    article = Article.query.get(id)
    return render_template("post_detail.html", article=article)


@app.route("/posts/<int:id>/delete")
def posts_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect("/posts")
    except:
        return "Error"


@app.route("/create-article", methods=["POST", "GET"])
def create_article():
    if request.method == "POST":
        title = request.form["title"]
        price = request.form["price"]

        article = Article(title=title, price=price)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect("/posts")
        except:
            return "ERROR"
    else:
        return render_template("create-article.html")


@app.route("/posts/<int:id>/update", methods=["POST", "GET"])
def posts_update(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.title = request.form["title"]
        article.price = request.form["price"]

        try:

            db.session.commit()
            return redirect("/posts")
        except:
            return "ERROR"
    else:

        return render_template("posts_update.html", article=article)


@app.route("/simple_chart")
def chart():
    articles = Article.query.order_by(Article.date.desc()).all()
    statistic_dict = {}
    statistic_date_array = []
    statistic_price_array = []

    for i in articles:
        if i.title not in statistic_dict:
            statistic_dict[i.title] = i.price
        elif i.title in statistic_dict:
            statistic_dict[i.title] = statistic_dict.get(i.title) + i.price

    for i in articles:

        statistic_date_array.append(str(i.date.day) + " " + str(i.date.month))
        statistic_price_array.append(i.price)

    legend = "Цена"
    labels = statistic_date_array
    values = statistic_price_array
    return render_template("chart.html", values=values, labels=labels, legend=legend)


if __name__ == "__main__":
    app.run(debug=True)
