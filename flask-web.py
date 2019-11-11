from flask import *
import hashlib
import sqlite3

app = Flask(__name__, static_url_path="", static_folder="static")

def gen_hash(str):
    hash = hashlib.sha256(str.encode())
    return hash.hexdigest()

def generate_token(userpasshash):
    # Generate token. use JWT in production
    SECRET = "dga38qw7rtiagfriegr9"
    string = userpasshash+SECRET
    token = gen_hash(string)
    return token

def is_authenticated(request):
    return generate_token(str(request.cookies.get('userid'))) == str(request.cookies.get('authCookie'))

def check_user(username,password):
    with sqlite3.connect('database.db') as conn:
        cur =conn.cursor()
        cur.execute("SELECT userId FROM users WHERE username = ? AND password = ?", (username,password ))
        userId = cur.fetchone()
        if userId :
            return userId
        else:
            return False


@app.route('/')
def home():
    if is_authenticated(request):
        return render_template('items.html')
    else:
        return redirect("/")

@app.route('/login/')
def render_login():
    return render_template('login.html')
@app.route('/register/')
def render_register():
    return render_template('register.html')

@app.route('/auth',methods = ['POST'])
def authenticate():
    user = str(request.form['username'])
    password = str(request.form['password'])
    userid = gen_hash(user+password)

    if not check_user(user,password):
        return redirect("/login")
    else:
        resp = make_response(redirect("/", code=302))
        cookie = generate_token(userid)
        print(cookie)
        resp.set_cookie('authCookie', cookie)
        resp.set_cookie('userid',userid)
        return resp

@app.route('/new-register',methods = ['POST'])
def new_register():
    username = str(request.form['username'])
    password = str(request.form['password'])
    name = str(request.form['firstname'])
    phone = str(request.form['phone'])
    address = str(request.form['address'])


    userId = gen_hash(username+password)

    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        data=cur.execute('select username from users')
        if username in data:
            return "user already exists"
        else:
            cur.execute('''INSERT INTO users (userId, username,password,name,phone,address) VALUES (?, ?, ?,?,?,?)''', (userId, username,password,name,phone,address))
            conn.commit()
            return "user created"



@app.route('/logout')
def logout():
    resp = make_response(redirect('/'))
    resp.set_cookie('authCookie', '',expires=0)
    resp.set_cookie('userid', '',expires=0)
    return resp


#===============================================
@app.route('/api/getpastries/')
def getPastries():
    with sqlite3.connect('database.db') as conn:
        cur =conn.cursor()
        cur.execute("SELECT * FROM products WHERE type = ?", ('pastries',))
        result = cur.fetchall()
        return jsonify(result)

@app.route('/api/getchocolates/')
def getChocolates():
    with sqlite3.connect('database.db') as conn:
        cur =conn.cursor()
        cur.execute("SELECT * FROM products WHERE type = ?", ('chocolates',))
        result = cur.fetchall()
        return jsonify(result)

@app.route('/api/getdairy/')
def getdairy():
    with sqlite3.connect('database.db') as conn:
        cur =conn.cursor()
        cur.execute("SELECT * FROM products WHERE type = ?", ('dairy',))
        result = cur.fetchall()
        return jsonify(result)

@app.route('/api/getsnacks/')
def getsnacks():
    with sqlite3.connect('database.db') as conn:
        cur =conn.cursor()
        cur.execute("SELECT * FROM products WHERE type = ?", ('snacks',))
        result = cur.fetchall()
        return jsonify(result)

@app.route('/api/buy/')
def buy():
    #ashjfgshjagfhjsda
    return jsonify({'pastries':'pas1'})

if __name__ == '__main__':
    app.run(debug=True)
