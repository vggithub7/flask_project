
from flask import Flask, url_for, render_template,request,session, redirect
import sqlite3
app = Flask(__name__)
app.secret_key = 'super secret key'
@app.route("/")
def home():
    return "<h1> Hello </h1>"

# @app.route("/<abcd>")
# def index():
#     return(render_template("index.html",data=abcd))

@app.route("/signup", methods=["GET","POST" ])
def signup():
    msg = None
    if(request.method=="POST"):
        if(request.form["username"]!="" and request.form["password"]!=""):
            username = request.form["username"]
            password = request.form["password"]
            conn = sqlite3.connect("signup.db")
            c = conn.cursor()
            c.execute("SELECT username FROM person")
            r=c.fetchall()
            for i in r:
                print(i)
                if username == i[0]:
                    msg = "Username Exists"
                    conn.commit()
                    conn.close()
                    return(render_template("signup.html",msg=msg))
            # conn = sqlite3.connect("signup.db")
            # c = conn.cursor()
            c.execute("INSERT INTO person (username, password, location) VALUES ('"+username+"', '"+password+"', 'Users/"+username+"') ")
            msg = "Account Created"
            conn.commit()
            conn.close()
        else:
            msg = "Something went wrong"

    return(render_template("signup.html",msg=msg))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=="POST":
        username=request.form['username']
        password=request.form['password']
        conn=sqlite3.connect('signup.db')
        c=conn.cursor()
        c.execute("SELECT * FROM person WHERE username = '"+username+"' and password = '"+password+"' ")
        r = c.fetchall()
        for i in r:
            if (username==i[0] and password==i[1]):
                if session:
                    try:
                        if session['logedin']==True:
                            msg='Log Out first'
                            return render_template('login.html',msg=msg)
                    except:
                        print('No Active users present...allowing new user to login')
                session['logedin'] = True
                session['username'] = username
                return redirect(url_for('about'))
            else:
                msg = 'Please enter valid username and password'
    return render_template('login.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/logout')
def logout():
    session.clear()
    msg='Logged Out successfully'
    return render_template('login.html',msg=msg)

@app.route('/users')
def users():
    conn=sqlite3.connect('signup.db')
    c=conn.cursor()
    c.execute("SELECT username FROM person")
    r=c.fetchall()
    conn.commit()
    conn.close()
    return render_template('users.html',r=r)

def print_hi(name):
    print(f'Hello {name}')

if __name__=='__main__':
    # print_hi('Jeff')
    app.run(debug=True)