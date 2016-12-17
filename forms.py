from flask import Flask, render_template, request, redirect
import pg

db = pg.DB(dbname='page_db')

app = Flask('mywiki')

@app.route('/<page_name>/edit', methods=['POST'])
def update_form(page_name):
    title = page_name
    page_content = request.form.get('page_content')
    last_modified_date = request.form.get('last_modified_date')
    author_last_modified = request.form.get('author_last_modified')
    db.insert(
        'page',
        title=title,
        page_content=page_content,
        last_modified_date=last_modified_date,
        author_last_modified=author_last_modified)
    return redirect('/')
# @app.route('/<page_name>')
# def placeholder():
#     page_title = request.query_string
#     if not page_title:
#         return redirect('/')
#     # query = 'select id,page_title,page_content,last_modified_date,author_last_modified from page where name = %s' % name
#     # cur.execute(query)
#     # entry = cur.fetchone()
#     # id = entry[0]
#     # name = entry[1]
#     # phone_number = entry[2]
#     # email = entry[3]
#     return render_template(
#         'placeholder.html',
#         page_title=page_title
#     )