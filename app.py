from flask import Flask, render_template, redirect, url_for,request,session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "muskanbegam"

#config database
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:muskan@localhost/goalsnap_db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False

#create database
db = SQLAlchemy(app)

#Database mODEL
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(25), unique= True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    
    def __init__(self,email,password):
        self.email = email
        self.set_password(password)
    
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
    
    
@app.route('/')
def home():
    if 'email' in session:
        return redirect('dashboard')
    print('Session cleared')
    return render_template("auth.html")

@app.route('/auth/<page>', methods=['GET','POST'])
def auth(page):
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        print(email,password)
        user = User.query.filter_by(email = email).first()
        print(user)

        if page == "login" :
            
            if user and user.check_password(password):
                session['email'] = email
                return redirect(url_for('dashboard'))
        else:
            
            if user:
                return render_template("dashboard.html", error="User already exists")
            else:
                new_user = User(email,password)
                db.session.add(new_user)
                db.session.commit()
                session['email'] = email
                return redirect('auth')  
    return render_template('auth.html') 
 


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', active_page='dashboard')

@app.route('/feed')
def feed():
    return render_template('feed.html', active_page='feed')

@app.route('/profile')
def profile():
    return render_template('profile.html', active_page='profile')

@app.route('/tasks')
def tasks():
    return render_template('tasks.html', active_page='tasks')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home', active_page='logout'))

     
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True)
    
    
    
           