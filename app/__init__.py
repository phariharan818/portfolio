import os
import datetime
from flask import Flask, render_template, redirect, url_for, request
from dotenv import load_dotenv
from peewee import (
    MySQLDatabase,
    SqliteDatabase,
    Model,
    CharField,
    TextField,
    DateTimeField,
)
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__, template_folder="../templates", static_folder="../static")

if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase("file:memory?mode=memory&cache=shared", uri=True)
else:
    mydb = MySQLDatabase(
        os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306,
    )


class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb


mydb.connect()
mydb.create_tables([TimelinePost])


NAMES = "Priya Hariharan"
URL = os.getenv("URL")


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title=NAMES, url=URL), 200


@app.route("/education")
def education():
    return render_template("education.html", title=NAMES, url=URL), 200


@app.route("/map")
def map():
    return render_template("map.html", title=NAMES, url=URL), 200


@app.route("/work")
def work():
    return render_template("work.html", title=NAMES, url=URL), 200


@app.route("/hobbies")
def hobbies():
    return render_template("hobbies.html", title=NAMES, url=URL), 200


@app.route("/api/timeline_post", methods=["POST"])
def post_time_line_post():
    errors = []
    # check all fields are present
    if (
        "content" not in request.form
        or "name" not in request.form
        or "email" not in request.form
    ):
        if "content" not in request.form:
            errors.append("Invalid content")
        if "name" not in request.form:
            errors.append("Invalid name")
        if "email" not in request.form:
            errors.append("Invalid email")
        return {"errors": errors}, 400

    name = request.form["name"]
    email = request.form["email"]
    content = request.form["content"]

    timeline_post = TimelinePost.create(name=name, email=email, content=content)

    return model_to_dict(timeline_post), 200


@app.route("/api/timeline_post", methods=["GET"])
def get_time_line_post():
    return {
        "timeline_posts": [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }, 200


@app.route("/timeline")
def timeline():
    return render_template("timeline.html", title="Timeline"), 200


@app.route("/<path:path>")
def catch_all(path):
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run()
