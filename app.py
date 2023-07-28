from datetime import timedelta
from flask import Flask, redirect, render_template, request, session, url_for
import db, string, random
app = Flask(__name__)
app.secret_key = "".join(random.choices(string.ascii_letters, k = 256))

@app.route('/', methods=['GET'])
def index():
    msg = request.args.get('msg')
    if msg == None:
        return render_template('index.html')
    else:
        return render_template('index.html', msg=msg)

#ログイン
@app.route('/', methods=['POST'])
def login():
    user_name = request.form.get('username')
    password = request.form.get('password')

    if db.login(user_name, password):

        return redirect(url_for('guest'))
    if db.admin_login(user_name, password):

        return redirect(url_for('admin'))
    else:
        error = "ユーザ名またはパスワードが違います。"

        input_data = {'user_name':user_name, 'password':password}
        return render_template('index.html', error=error, data=input_data)

#利用者
@app.route("/guest", methods=['GET'])
def guest():
    return render_template("mypage.html")

#管理者
@app.route('/admin', methods=['GET'])
def admin():
    return render_template("adminhome.html")


@app.route('/register')
def register_form():
    return render_template('register.html')

#利用者登録
@app.route('/register_exe', methods=['POST'])
def register_exe():
    user_name = request.form.get('username')
    password = request.form.get('password')
    if user_name == '':
        error = 'ユーザ名が未入力です'
        return render_template('register.html', error=error)
    if password == '':
        error = 'パスワードが未入力です'
        return render_template('register.html', error=error)
    count = db.insert_user(user_name, password)
    if count == 1:
        msg = '登録が完了しました。'
        return redirect(url_for('index', msg=msg))
    else:
        error = '登録に失敗しました。'
        return render_template('register.html', error=error)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))

@app.route("/booklist")
def book_list():
    book_list = db.select_all_book()
    return render_template("booklist.html",book=book_list)

@app.route("/search_book", methods=['POST'])
def search_book():
    title = request.form.get('title')
    print(title)
    book_list = db.search_title_book(title)
    return render_template('booklist.html', book=book_list)

@app.route("/insert_book")
def insert_book():
    return render_template("insert_book.html")

#図書登録
@app.route("/insert_book_exe", methods=['POST'])
def insert_book_exe():
    title = request.form.get("title")
    author = request.form.get("author")
    publisher = request.form.get("publisher")
    isbn = request.form.get("isbn")
    genre = request.form.get("genre")
    if title == '':
        error = 'タイトルが未入力です'
        return render_template('insert_book_exe.html', error=error)
    if author == '':
        error = '著者が未入力です'
        return render_template('insert_book_exe.html', error=error)
    if publisher == '':
        error = '出版社が未入力です'
        return render_template('insert_book_exe.html', error=error)
    if isbn == '':
        error = 'isbnが未入力です'
        return render_template('insert_book_exe.html', error=error)
    if genre == '':
        error = 'ジャンルが未入力です'
        return render_template('insert_book_exe.html', error=error)
    
    session['title'] = title
    session['author'] = author
    session['publisher'] = publisher
    session['isbn'] = isbn
    session['genre'] = genre
    
    return render_template('insert_book_exe.html', title=title, author=author, publisher=publisher, isbn=isbn, genre=genre)
    
@app.route("/insert_book_end")
def insert_book_end():
    
    title  = session.get('title')
    author = session.get('author')
    publisher = session.get('publisher')
    isbn = session.get('isbn')
    genre = session.get('genre')
    
    count = db.insert_book(title,author,publisher,isbn,genre)
    
    print(count)
    
    if count == 1:
        msg = '登録が完了しました。'
        return render_template('insert_book_end.html', msg=msg)
    else:
        error = '登録が失敗しました。'
        return render_template('insert_book.html',error=error)
    

# @app.route("/edit_book", methods=["POST"])
# def edit_book():
#     title = request.form.get("title")
#     author = request.form.get("author")
#     publisher = request.form.get("publisher")
#     isbn = request.form.get("isbn")
#     genre = request.form.get("genre")
    
#     session['title'] = title
#     session['author'] = author
#     session['publisher'] = publisher
#     session['isbn'] = isbn
#     session['genre'] = genre
#     return render_template("edit_book.html", title=title, author=author, publisher=publisher, isbn=isbn, genre=genre)


# @app.route("/edit_book_exe", methods=["POST"])
# def edit_book_exe():
#     return render_template("edit_book_exe.html")


@app.route("/delete_book_list")
def delete_book_list():
    delete_book_list = db.select_all_book()
    return render_template("delete_book_list.html",book=delete_book_list)

# @app.route("/delete_book_exe",methods=['POST'])
# def delete_book_exe():
#     title = request.form.get("title")
#     author = request.form.get("author")
#     publisher = request.form.get("publisher")
#     isbn = request.form.get("isbn")
#     genre = request.form.get("genre")
    
#     session['title'] = title
#     session['author'] = author
#     session['publisher'] = publisher
#     session['isbn'] = isbn
#     session['genre'] = genre
#     return render_template("delete_book_exe.html", title=title, author=author, publisher=publisher, isbn=isbn, genre=genre)

@app.route("/delete_book_end",methods=['POST'])
def delete_book_end():
    isbn = request.form.get("isbn")
    db.delete_book(isbn)
    return render_template("delete_book_end.html")

if __name__ == "__main__":
    app.run(debug=True)