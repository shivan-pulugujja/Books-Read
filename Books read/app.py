from operator import and_
from flask import Flask, render_template, request, session
from flask.helpers import flash, url_for
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
        
    # user = Users.query.all()
    # return render_template("user.html",users=user)


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
        if 'username' in session:
            username = session['username']
            return render_template("index.html",uname = username,flag = True,books=book)
        else:
            return render_template("index.html",flag = False,books=book)

    else:
        return redirect('home')

@app.route("/book/details/<id>",methods=['POST','GET'])
def get_book_details(id):
    det = Bookdetails.query.filter(Bookdetails.id==id).all()
    total_reviews = reviews.query.filter(reviews.bookId==id).all()
    session['bookid'] = id
    flag_review = False
    book_del = True
    if 'username' in session:
        user = session['username']
        try:
            rev = reviews.query.filter(and_(reviews.bookId==id,reviews.uname==user)).first()
            if rev.uname != None:
                flag_review = False
        except Exception as e:
            print("exception while clicked on id = ",e)
            flag_review = True

        try:
            s = shelf.query.filter(and_(shelf.bookId==id, shelf.uname==user)).first()
            if s.bookId != None:
                book_del = False
        except:
            book_del = True

    
        return render_template('details.html',reviews=total_reviews,uname=user,flag_review=flag_review,flag=True,details=det,book_del = book_del)
    else:
        return render_template('details.html',reviews=total_reviews,flag_review=flag_review,flag=False,details=det,book_del = book_del)


@app.route("/review", methods=['POST','GET'])
def review():
    if request.method == 'GET':
        return render_template('details.html')
    else:
        review = request.form.get('review')
        rating = request.form.get('rating')
        user = session['username']
        bookid = session['bookid']
        print("from /review , user= ",user," book = ",bookid)
        r = reviews(bookId=bookid,uname=user,review=review,rating=int(rating))
        db.session.add(r)
        db.session.commit()
        book_del= True
        try:
            s = shelf.query.filter(and_(shelf.bookId==id, shelf.uname==user)).first()
            if s.bookId != None:
                book_del = False
        except:
            book_del = True
        det = Bookdetails.query.filter(Bookdetails.id==bookid).all()
        total_reviews = reviews.query.filter(reviews.bookId==bookid).all()
        return render_template('details.html', reviews=total_reviews, flag_review=False, uname=user, flag=True, details=det,book_del=book_del)


@app.route('/shelfsubmit', methods=['POST','GET'])
def shelfsubmit():
    if request.method == 'GET':
        return redirect('home')
    else:
        bookid = session['bookid']
        det = Bookdetails.query.filter(Bookdetails.id==bookid).all()
        total_reviews = reviews.query.filter(reviews.bookId==bookid).all()
        book_del = True
        flag_review = False
        if 'username' in session:
            count = request.form.get('shelf')
            user = session['username']
            
            try:
                s = shelf.query.filter(and_(shelf.bookId==bookid, shelf.uname==user)).delete()
                db.session.commit()
                print("*************",s,type(s))
                if s == 0:
                    print(s.uname)
                # print("shelf submit files = ",s.uname,s.bookId)
                flash("Book is removed from the shelf")
                book_del = True
            except Exception as e:
                print("exception from shelf submit = ",e)
                s = shelf(bookId=bookid, uname=user, bookCount=count)
                db.session.add(s)
                db.session.commit()
                book_del = False
                flash("Book is added into Shelf")
                
            try:
                rev = reviews.query.filter(and_(reviews.bookId==bookid,reviews.uname==user)).first()
                if rev.uname != None:
                    flag_review = False
            except Exception as e:
                print("exception while clicked on id = ",e)
                flag_review = True
            
            return render_template('details.html',reviews=total_reviews,uname=user,flag_review=flag_review,flag=True,details=det,book_del = book_del)
            # return render_template('index.html', form=form)

        else:
            flash("Please login or register to add the book")
            return render_template('details.html',reviews=total_reviews,flag_review=flag_review,flag=False,details=det,book_del = book_del)

@app.route("/shelfpage",methods=['POST','GET'])
def shelfpage():
    if 'username' in session:
        user = session['username']
        try:
            books = shelf.query.filter(shelf.uname==user).all()
            user = session['username']
            shelfbooks = []
            for book in books:
                bookid=book.bookId
                det = Bookdetails.query.filter(Bookdetails.id==bookid).all()
                shelfbooks.append(det)

            # print("shelfbooks = ",shelfbooks)
            return render_template("shelf.html",books=shelfbooks,flag=True,uname=user)
        except:
            return render_template('shelf.html',msg=True)
    else:
        pass

@app.route("/admin")
def admin():
    user = Bookdetails.query.all()
    return render_template("user.html",users=user)