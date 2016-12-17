from flask import Flask, render_template, request
import mysql.connector

app = Flask('mywiki')

conn = mysql.connector.connect(
    user='root',
    password='',
    host='127.0.0.1',
    database='mywiki')

cur = conn.cursor()

@app.route("/")
def home():
    query = "SELECT id,title FROM page"
    cur.execute(query)
    list = cur.fetchall()
    return render_template("wiki_home.html", title_list=list, title="Wiki Pages")

@app.route('/<page_name>')
def placeholder(page_name):
    return render_template('placeholder.html', title = page_name)

@app.route('/<page_name>/edit')
def update_form(page_name):
    title = page_name
    if not title:
        return redirect('/')
    sql = "SELECT COUNT(1) FROM page WHERE title = '%s'" %title
    cur.execute(sql)
    if cur.fetchone()[0]:
        query = 'select title,page_content,last_modified_date,author_last_modified from page where title = %s' % title
        cur.execute(query)
        entry = cur.fetchone()
        title = entry[0]
        page_content = entry[1]
        last_modified_date = entry[2]
        author_last_modified = entry[3]

        return render_template(
            'edit.html',
            page_title='Edit Page',
            title=title,
            page_content=page_content,
            last_modified_date=last_modified_date,
            author_last_modified=author_last_modified)
    else:
        return render_template(
            'edit.html',
            page_title='Edit Page',
            title=title,
        )


if __name__ == "__main__":
    app.run(debug=True)
cur.close()

conn.close()
