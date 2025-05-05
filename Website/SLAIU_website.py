from flask import Flask, render_template, flash, redirect, request, url_for, send_file
from form import RegistrationForm, LoginForm
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from sqlalchemy.orm import sessionmaker, relationship
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, and_, null, ForeignKey, select
import datetime


# with open('secrets/pwdb', 'r') as f:
#     password = f.read()

password = "DBPasswordhere"

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Key'

app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://slaiu-db:{password}@mysql-slaiu-db.alwaysdata.net:3306/slaiu-db_data"
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return accounts.query.get(int(user_id))


class lessons(db.Model):
    lesson_id = db.Column(db.Integer, primary_key=True)
    lesson = db.Column(db.String(255))
    hours = db.Column(db.Integer)
    prices = db.Column(db.Integer)
    minimumage = db.Column(db.Integer)
    provider_id = db.Column(db.Integer, ForeignKey('providerinfo.ID'))
    lesson_type = db.Column(db.String(20))
    link = db.Column(db.String(800))
    available_from = db.Column(db.Date)


    def __repr__(self) -> str:
        return f"Lesson name: {self.lesson}"

class accounts(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)

    def get_id(self):
        return self.user_id

class providerinfo(db.Model):
    ID = db.Column(db.Integer, primary_key=True, unique=True)
    Link = db.Column(db.String(250))
    provider_name = db.Column(db.String(50))
    location = db.Column(db.String(300))


    def get_id(self):
           return (self.user_id)

    
# Route setup

@app.route('/')

def homepage():
    return render_template('home.html')

@app.route('/findlessons', methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":

        time = request.form["input_time"]
        date = request.form["input_date"]
        maxprice = request.form["input_prices"]
        age = request.form["input_ages"]
        type = request.form["types"]

        if(time == ''):
            time = '100000000'
        if(date == ''):
            date = '2024-10-02'
        if(maxprice == ''):
            maxprice = '100000000'
        if(age == ''):
            age = '100000000'
    

    

        primary_matches = db.session.query(lessons, providerinfo).join(providerinfo).where(lessons.hours <= time,
                                    lessons.available_from >= date,
                                    lessons.prices <= maxprice,
                                        lessons.minimumage <= age,
                                        lessons.lesson_type == type).all()

        
        if(time == '100000000'):
            time = null()
        if(date == "2024-10-02"):
            date = null()
        if(maxprice == '100000000'):
            maxprice = null()
        if(age == '100000000'):
            age = null()


        possibly_relevant = db.session.query(lessons, providerinfo).join(providerinfo).where(lessons.hours == time,
                                           lessons.available_from == date,
                                            lessons.prices == maxprice,
                                              lessons.minimumage == age).all()

        nulls = db.session.query(lessons, providerinfo).join(providerinfo).where(lessons.hours == null(),
                                           lessons.available_from == null(),
                                            lessons.prices == null(),
                                              lessons.minimumage == null(),
                                              lessons.lesson_type == null()).all()
        
        
        

        return render_template('Findlessons.html', primary_matches = primary_matches, nulls = nulls, possibly_relevant = possibly_relevant)
    
    return render_template('Findlessons.html')

@app.route('/show-all-results', methods=['GET', 'POST'])
def allresults():
    results = db.session.query(lessons, providerinfo).join(providerinfo)
    return render_template('Findlessons.html', all_lessons = results)

@app.route('/about')
def about():
    return render_template('About.html')


@app.route('/contact')
def contact():
    return render_template('Contact.html')

@app.route('/help')
def help():
    return render_template('Help.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        if accounts.query.where(and_(accounts.username == username, accounts.email == email, accounts.password == password)).all():
            print(accounts.query.where(and_(accounts.username == username, accounts.email == email, accounts.password == password)).all())
            flash("This account already exists")
            return redirect('/')
        if accounts.query.where(or_(accounts.username == username, accounts.email == email, accounts.password == password)).all():
            flash("An account already exists with these details")
            return redirect('/')
        else:
            db.session.add(accounts(username=username, email=email, password=password))
            db.session.commit()
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect('/')
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        
        account = accounts.query.filter_by(username=form.username.data).first() 
        if account:
            if form.password.data == account.password:
                login_user(account)
                if(form.remember.data == True):
                    app.config['REMEMBER_COOKIE_DURATION'] = datetime.timedelta(days=30)
                else:
                    app.config['REMEMBER_COOKIE_DURATION'] = datetime.timedelta(seconds=10)
                flash('Your Login is Successful!')
                return redirect('/')
            else:
                flash("Your password is not correct: ")
        else:
            flash("Account does not exist, please register for a new account: ")
        
    return render_template('login.html', title='Login', form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/songs')
def songs():
    return render_template('songs.html')




if __name__ == "__main__":

    app.run(debug=True)

