import os, psycopg2, string, random, hashlib

def get_connection():
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection
def get_salt():
    charset = string.ascii_letters + string.digits
    salt = ''.join(random.choices(charset, k=30))
    return salt
def get_hash(password, salt):
    b_pw = bytes(password, 'utf-8')
    b_salt = bytes(salt, 'utf-8')
    hashed_password = hashlib.pbkdf2_hmac("sha256", b_pw, b_salt, 1000).hex()
    return hashed_password
def insert_user(user_name, password):
    sql = "INSERT INTO users VALUES(default, %s, %s, %s)"
    salt = get_salt()
    hashed_password = get_hash(password, salt)
    try :
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (user_name, hashed_password, salt))
        count = cursor.rowcount
        connection.commit()
    except  psycopg2.DatabaseError:
        count = 0
    finally:
        cursor.close()
        connection.close()
    return count

def login(user_name, password):
    sql = 'SELECT hashed_password, salt FROM users WHERE name = %s'
    flg = False

    try :
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(sql, (user_name,))
        user = cursor.fetchone()

        if user != None:
            
            salt = user[1]

            hashed_password = get_hash(password, salt)

            if hashed_password == user[0]:
                flg = True

            if  flg == False:
                sql = 'SELECT hashed_password, salt FROM users WHERE name = %s'
                flg = True

    except psycopg2.DatabaseError :
        flg = False

    finally :
        cursor.close()
        connection.close()

    return flg

def get_connection():
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection

def insert_book(title,author,publisher,isbn,genre):
    sql = "INSERT INTO book VALUES(default, %s, %s, %s, %s, %s)"
    try :
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql,(title,author,publisher,isbn,genre))
        count = cursor.rowcount
        connection.commit()
    except psycopg2.DatabaseError:
        count = 0
    finally:
        cursor.close()
        connection.close()
    return count

def select_all_book():
    connection = get_connection()
    cursor = connection.cursor()
    sql = "SELECT title,author,publisher,isbn,genre FROM book"
    
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    cursor.close()
    connection.close()
    return rows

def search_title_book(title):
    connection = get_connection()
    cursor = connection.cursor()
    sql = "SELECT title,author,publisher,isbn,genre FROM book WHERE title LIKE %s"
    
    search_pattern = f'%{title}%'

    cursor.execute(sql, (search_pattern,))
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows

def delete_book(isbn):
    connection = get_connection()
    cursor = connection.cursor()
    sql = "DELETE FROM book WHERE isbn = %s"
    
    cursor.execute(sql,(isbn,))
    
    connection.commit()
    
    cursor.close()
    connection.close()
    
def search_book(keyword):
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'SELECT * FROM book WHERE title LIKE %s'
  
    pattern=f"%{keyword}%"
  
    cursor.execute(sql, (pattern,))
  
    rows = cursor.fetchall()

    cursor.close()
    connection.close()
    return rows
    
def edit_book(title,author,publisher,isbn,genre):
    connection = get_connection()
    cursor = connection.cursor()
    sql = "UPDATE book SET title = %s, author = %s, publisher = %s, genre = %s WHERE isbn = %s"
    
    cursor.execute(sql, (title,author,publisher,isbn,genre))
    
    connection.commit()
    
    cursor.close()
    connection.close()
    
def admin_login(user_name, password):
    sql = 'SELECT hashed_password, salt FROM admin WHERE name = %s'
    flg = False

    try :
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(sql, (user_name,))
        user = cursor.fetchone()

        if user != None:
        
            salt = user[1]

            hashed_password = get_hash(password, salt)

            if hashed_password == user[0]:
                flg = True

    except psycopg2.DatabaseError :
        flg = False

    finally :
        cursor.close()
        connection.close()

    return flg