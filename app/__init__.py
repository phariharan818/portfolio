import os
import datetime
from flask import Flask, render_template, redirect, url_for, request
from dotenv import load_dotenv
from peewee import *
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__, template_folder="../templates", static_folder="../static")

mydb = MySQLDatabase(
    os.getenv("MYSQL_DATABASE"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    host=os.getenv("MYSQL_HOST"),
    port=3306
)

print(mydb)

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])


NAMES = "Priya's Portfolio"
URL = os.getenv("URL")


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title=NAMES, url=URL)


@app.route("/education")
def education():
    return render_template("education.html", title=NAMES, url=URL)


@app.route("/map")
def map():
    return render_template("map.html", title=NAMES, url=URL)


@app.route("/work")
def work():
    return render_template("work.html", title=NAMES, url=URL)


@app.route("/hobbies")
def hobbies():
    return render_template("hobbies.html", title=NAMES, url=URL)


@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    timeline_post = TimelinePost.create(name=name, email=email, content=content)

    return model_to_dict(timeline_post)


@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

@app.route('/timeline')
def timeline():
    return render_template('timeline.html', title='Timeline')


@app.route("/<path:path>")
def catch_all(path):
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run()
