from flask import Flask, render_template, request
from wiki_linkify import wiki_linkify
import mysql.connector
from jinja2 import Environment, FileSystemLoader

app = Flask('mywiki')

conn = mysql.connector.connect(
    user='root',
    password='',
    host='127.0.0.1',
    database='mywiki')

cur = conn.cursor()

# Environment.filters['wiki_linkify)'] = wiki_linkify

# loader = FileSystemLoader('/tmp')
env = Environment(loader=FileSystemLoader('templates'))
env.filters['wiki_linkify'] = wiki_linkify
view = env.get_template('view.html')


@app.route("/")
def home():
    query = "SELECT id,title FROM page"
    cur.execute(query)
    list = cur.fetchall()
    return render_template("wiki_home.html", title_list=list, title="Wiki Pages")


@app.route('/<page_name>')
def placeholder(page_name):
    title = page_name
    sql = "SELECT COUNT(1) FROM page WHERE title = '%s'" % title
    cur.execute(sql)
    if cur.fetchone()[0]:
        query = "select page_content,last_modified_date,author_last_modified from page where title = '%s'" % title
        cur.execute(query)
        entry = cur.fetchone()
        page_content = entry[0]
        last_modified_date = entry[1]
        author_last_modified = entry[2]

        return view.render(
            page_title=page_name,
            title=page_name,
            page_content=page_content,
            last_modified_date=last_modified_date,
            author_last_modified=author_last_modified)
    else:
        return render_template('placeholder.html', title=page_name)


@app.route('/<page_name>/edit')
def update_form(page_name):
    title = page_name
    if not title:
        return redirect('/')
    sql = "SELECT COUNT(1) FROM page WHERE title = '%s'" % title
    cur.execute(sql)
    if cur.fetchone()[0]:
        query = 'select page_content,last_modified_date,author_last_modified from page where title = %s' % title
        cur.execute(query)
        entry = cur.fetchone()
        page_content = entry[0]
        last_modified_date = entry[1]
        author_last_modified = entry[2]

        return view.render(
            page_title=page_name,
            title=page_name,
            page_content=page_content,
            last_modified_date=last_modified_date,
            author_last_modified=author_last_modified)
    else:
        return render_template(
            'edit.html',
            page_title='Edit Page',
            title=page_name,
        )


@app.route('/<page_name>/save', methods=['POST'])
def submit_new_page(page_name):
    title = page_name
    page_content = request.form.get('page_content')
    last_modified_date = request.form.get('last_modified_date')
    author_last_modified = request.form.get('author_last_modified')
    query = (
        "insert into page (title, page_content, last_modified_date, author_last_modified) values(\"%s\", \"%s\", \"%s\", \"%s\")" % (
            title, page_content, last_modified_date, author_last_modified))
    cur.execute(query)
    conn.commit()
    return render_template(
        "/view",
        title=page_name,
        page_content=page_content,
        last_modified_date=last_modified_date,
        author_last_modified=author_last_modified)


if __name__ == "__main__":
    app.run(debug=True)
cur.close()

conn.close()
