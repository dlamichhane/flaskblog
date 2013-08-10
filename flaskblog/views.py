#imports
from flaskblog import app, db, login_manager
from flask import render_template, request, flash, url_for, g, session, redirect
from form import LoginForm, PostForm, TagForm, SearchForm
from models import db, Admin, Tag, Post, Pagination
from flask.ext.login import login_user, logout_user, current_user, login_required
from config import PER_PAGE, MAX_SEARCH_RESULTS


@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')


@app.route('/posts', defaults={'page': 1})
@app.route('/posts/page/<int:page>')
def posts(page):
	count =  db.session.query(Post).count()
	posts = Post.query.limit(PER_PAGE).offset(page)
	if not posts and page != 1:
		abort(404)
	pagination = Pagination(page, PER_PAGE, count)
	return render_template('posts.html', pagination=pagination, posts=posts)


@app.route('/post/<int:id>')
def post(id):
	post = Post.query.filter_by(id=id).first()
	return render_template('post.html', post=post)


@login_manager.user_loader
def load_user(user):
	return Admin.query.get(user)


@app.before_request
def before_request():
	g.user = current_user
	g.search_form = SearchForm()


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_user(form.admin)
        flash("Logged in successfully.")
        return redirect(request.args.get("next") or url_for("index"))
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
	flash("Logout successfully")
	logout_user()
	return redirect(url_for("index"))


@app.route('/addpost', methods=["GET", "POST"])
@login_required
def addpost():
	form = PostForm(csrf_enabled=False)
	form.tag.choices = [(str(tag.id), str(tag.tag)) for tag in Tag.query.all()]
	if request.method == "POST":
		if form.validate() == False:
			return render_template('addpost.html', form = form)
		else:
			tags = [ Tag.query.filter_by(id=tag_id).first() for tag_id in form.tag.data ]
			post = Post(form.title.data, form.text.data, tags)
			db.session.add(post)
			# # db.session.execute(posts_tags.insert(), params={"post_id": 1, "tag_id": 1})
      		db.session.commit()
      		flash('Posted successfully')
      		return render_template('index.html')
	return render_template("addpost.html", form = form)


@app.route('/editpost/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):	
	if request.method == 'POST':
		form = PostForm()
		form.tag.choices = [(str(tag.id), str(tag.tag)) for tag in Tag.query.all()]
		if form.validate() == False:
			return render_template('editpost.html', form=form)
		else:	
			tags = [ Tag.query.filter_by(id=tag_id).first() for tag_id in form.tag.data ]
			post = Post.query.filter_by(id=id).first()
			post.title = form.title.data
			post.text = form.text.data
			post.tags = tags
			db.session.merge(post)
			db.session.commit()
			flash('Post updated successfully')
			return render_template('index.html')
	elif request.method == 'GET':
		post = Post.query.filter_by(id=id).first()
		form = PostForm(id=post.id, title=post.title, text=post.text)
		form.tag.choices = [(str(tag.id), str(tag.tag)) for tag in Tag.query.all()]
		return render_template('editpost.html', post_id= post.id, form=form)


@app.route('/deletepost/<int:id>')
@login_required
def delete_post(id):
	post = Post.query.filter_by(id=id).first()
	db.session.delete(post)
	db.session.commit()
	return render_template('index.html')


@app.route('/addtag', methods=['GET', 'POST'])
@login_required
def addtag():
	form = TagForm()
	if request.method == "POST":
		if form.validate() == False:
			return render_template('addtag.html', form=form)
		else:
			tag = Tag(form.tag.data)
			db.session.add(tag)
			db.session.commit()
			flash('Tag created successfully')
			return render_template('tags.html', tags = Tag.query.all())
	return render_template("addtag.html", form=form)


@app.route('/tags', methods=['GET', 'POST'])
def tags():
	tags = Tag.query.all()
	if tags is None:
		flash("No tag created yet")
		return render_template('addtag.html')
	return render_template('tags.html', tags=tags)


@app.route('/tags/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_tag(id):
	if request.method == 'POST':
		form = TagForm()
		if form.validate() == True:
			tag = Tag.query.filter_by(id=id).first()
			tag.tag = form.tag.data
			db.session.merge(tag)
			db.session.commit()
			flash('Tag updated successfully')
			return render_template('tags.html', tags = Tag.query.all())
	elif request.method == 'GET':
		tag = Tag.query.get(id)
		form = TagForm(id=tag.id, tag=tag.tag)
		return render_template('edittag.html', tag_id= tag.id, form=form)


@app.route('/delete_tag/<int:id>')
@login_required
def delete_tag(id):
    tag = Tag.query.filter_by(id=id).first()
    db.session.delete(tag)
    db.session.commit()
    return render_template('tags.html', tags = Tag.query.all())


@app.route('/users/', defaults={'page': 1})
@app.route('/users/page/<int:page>')
def show_users(page):
    count = count_all_users()
    users = get_users_for_page(page, PER_PAGE, count)
    if not users and page != 1:
        abort(404)
    pagination = Pagination(page, PER_PAGE, count)
    return render_template('users.html',
        pagination=pagination,
        users=users
    )


@app.route('/search', methods=['POST'])
@login_required
def search():
	if request.method == 'POST':
		if g.search_form.validate() == False:
			return render_template('index.html', form = g.search_form)
		else:
			results = Post.query.whoosh_search(g.search_form.search.data, MAX_SEARCH_RESULTS).all()
			return render_template('search.html', query = g.search_form.search.data, results = results)
	return render_template('index.html', form = form)