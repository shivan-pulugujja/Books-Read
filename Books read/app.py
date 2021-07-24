from operator import and_
from flask import Flask, render_template, request, session
from flask.helpers import url_for
from werkzeug.utils import redirect
from models import *
import pandas as pd

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://fccbyzntfcsaty:65a0a51aad07e4313bc1f0940d21734ba971ee50a18010165e43b4e96d279ab0@ec2-52-0-67-144.compute-1.amazonaws.com:5432/d6jqivik227nb7'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.secret_key = "any random string"

with app.app_context():
    db.create_all()

# @app.route("/")
# def index():
#     df = pandas.read_csv('books.csv', index_col='isbn')
#     for ind in df.index:
#         try:
#             b = Bookdetails(id=ind,title=df['title'][ind],author=df['author'][ind],year=str(df['year'][ind]))
#             db.session.add(b)
#         except Exception as e:
#             print("pandas ind",e)
#     db.session.commit()
#     user = Bookdetails.query.all()
#     return render_template("user.html",users=user)



@app.route("/home")
def home():
    flag = False
    if 'username' in session:
        username = session['username']
        flag = True
        return render_template("index.html",uname = username,flag = flag)

    return render_template("index.html",flag=flag)

@app.route("/register", methods=["POST","GET"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        uname = request.form.get("uname")
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        email = request.form.get("email")
        pwd = request.form.get("pwd")
        try:
            existing_user = Users.query.filter(Users.uname==uname).first()
            print("exitisting user = ",existing_user.uname)
            if existing_user.uname != None:
                session['username'] = uname
                return render_template("register.html",flag=True)               
        except Exception as e:
            print("register exception = ",e)
            u = Users(uname=uname,firstname=fname,lastname=lname,email=email,pwd=pwd)
            session['username'] = uname
            db.session.add(u)
            db.session.commit()
            
            return redirect('login')
        
    user = Users.query.all()
    return render_template("user.html",users=user)


@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == "GET":
        return render_template("login.html",flag=False)
    else:
        uname = request.form.get("uname")
        pwd = request.form.get("pwd")
        try:
            uname = Users.query.filter(and_(Users.uname==uname,Users.pwd==pwd)).first()
            print("uname = ",uname.uname)
            session['username'] = uname.uname
            return redirect("home")
        except Exception as e:
            print("login exception = ",e)
            return render_template("login.html",flag=True)

    
@app.route("/logout",methods=["POST","GET"])
def logout():
    session.pop('username',None)
    return redirect('home')

@app.route("/profile",methods=["POST","GET"])
def profile():
    if 'username' in session:
        username = session['username']
        return render_template("profile.html",uname = username)
    else:
        return redirect('home')

@app.route("/book", methods=["POST","GET"])
def book():
    if request.method == "POST":
        det = request.form.get("bookvalue")
        tag = '%'+det+'%'
        book1 = Bookdetails.query.filter(Bookdetails.id.ilike(tag)).all()
        book2 = Bookdetails.query.filter(Bookdetails.title.ilike(tag)).all()
        book3 = Bookdetails.query.filter(Bookdetails.author.ilike(tag)).all()
        book4 = Bookdetails.query.filter(Bookdetails.year.ilike(tag)).all()
        book = book1+book2+book3+book4
        username = session['username']
        flag = True
        return render_template("index.html",uname = username,flag = flag,books=book)
    else:
        return redirect('home')
