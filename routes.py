from flask import Flask, render_template, request, redirect
from wiki_linkify import wiki_linkify
from jinja2 import Environment, FileSystemLoader
from page import *

app = Flask('mywiki')


@app.route("/")
def home():
    list = Page.getObjects()
    return render_template("wiki_home.html", title_list=list, title="Wiki Pages")


@app.route('/<page_name>')
def placeholder(page_name):
    page = Page()
    page.title = page_name
    exists = page.placeHolder()
    if exists:
        return view.render(
            page_title=page.title,
            title=page.title,
            page_content=page.page_content,
            last_modified_date=page.last_modified_date,
            author_last_modified=page.author_last_modified)
    else:
        return render_template('placeholder.html', title=page.title)


@app.route('/<page_name>/edit')
def update_form(page_name):
    page = Page()
    page.title = page_name
    page.page_content = request.form.get('page_content')
    page.update()
    if page.page_content:
        return render_template(
            "edit.html",
            page_title=page.title,
            title=page.title,
            page_content=page.page_content,
        )
    else:
        return render_template(
            'edit.html',
            page_title='Edit Page',
            title=page.title,
        )


@app.route('/<page_name>/save', methods=['POST', 'GET'])
def save(page_name):
    page = Page()
    page.title = page_name
    page.page_content = request.form.get('page_content')
    page.author_last_modified = request.form.get('author_last_modified')
    page.save()
    return view.render(
        title=page.title,
        page_content=page.page_content,
        last_modified_date=page.last_modified_date,
        author_last_modified=page.author_last_modified)


conn = Database.getConnection()
cur = conn.cursor()
env = Environment(loader=FileSystemLoader('templates'))
env.filters['wiki_linkify'] = wiki_linkify
view = env.get_template('view.html')
cur.close()
conn.close()

if __name__ == "__main__":
    app.run(debug=True)
cur.close()

conn.close()
