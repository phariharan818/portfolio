import os
import datetime
from flask import Flask, render_template, redirect, url_for, request
from dotenv import load_dotenv
from peewee import *
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__, template_folder="../templates", static_folder="../static")

if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
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


NAMES = "Priya Hariharan"
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


@app.route("/timeline", methods=["POST"])
def post_time_line_post():
    print("Received POST request")
    name = request.form.get("name")
    email = request.form.get("email")
    content = request.form.get("content")
    print(f"Form Data - name: {name}, email: {email}, content: {content}")

    if not all([name, email, content]):
        print("Invalid form data")
        return redirect(url_for("timeline"))

    try:
        timeline_post = TimelinePost.create(name=name, email=email, content=content)
        print("Post created successfully:", timeline_post)
    except Exception as e:
        print("Error creating post:", e)

    return redirect(url_for("timeline"))


@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

@app.route("/delete_post", methods=["POST"])
def delete_post():
    post_id = request.form.get("post_id")
    try:
        post = TimelinePost.get_by_id(post_id)
        post.delete_instance()
    except TimelinePost.DoesNotExist:
        return {"error": "Post does not exist"}, 404

    return redirect(url_for("timeline"))

@app.route("/timeline", methods=["GET"])
def timeline():
    posts = [p for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())]

    return (
        render_template(
            "timeline.html",
            title="Timeline",
            posts=posts,
            url=URL,
        )
    )


@app.route("/<path:path>")
def catch_all(path):
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run()
