from flask import Blueprint, render_template, redirect, url_for, request
from sqlalchemy import select, delete
from app import db
from app.models import User, Post

bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/posts", methods=["GET", "POST"])
def posts():
    if request.method == "POST":
        post_id = request.form.get("post_id")
        if post_id:
            stmt = delete(Post).where(Post.id == int(post_id))
            db.session.execute(stmt)
            db.session.commit()
        return "", 200  # Respond OK to fetch

    stmt = select(Post).order_by(Post.id.desc())
    posts = db.session.scalars(stmt).all()
    return render_template("posts.html", posts=posts)


@bp.route("/posts/create", methods=["GET", "POST"])
def create_post():
    if request.method == "POST":
        username = request.form["username"]
        title = request.form["title"]
        content = request.form["content"]

        user = db.session.scalar(
            select(User).where(User.username == username)
        )

        if not user:
            user = User(username=username)
            db.session.add(user)

        post = Post(title=title, content=content, author=user)
        db.session.add(post)
        db.session.commit()

        return redirect(url_for("main.posts"))

    return render_template("create_post.html")
