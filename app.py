from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy 
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'abc123'

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/your_weather'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define User model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    fullname = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

#home
@app.route('/')
def index():
    return render_template('main.html')

#login
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
   
    user = User.query.filter_by(email=email).first()
   
    if user and check_password_hash(user.password, password):
        session['email'] = email
        flash('Login successful!', 'success')
        return redirect(url_for('homepage'))
    else:
        flash('Invalid username or password', 'error')
        return redirect(url_for('index'))

#dashboard
@app.route('/homepage')
def homepage():
    if 'email' not in session:
        flash('Please log in first', 'error')
        return redirect(url_for('index'))
    return render_template('homepage.html')

#register    
@app.route('/register', methods=['POST'])
def register():
    fullname = request.form['fullname']
    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email).first()

    if user:
        flash('An account with this email already exists', 'error')
        return redirect(url_for('index'))
    else:
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(
            fullname=fullname, 
            password=hashed_password,
            email=email
        )
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('index'))

#Logout
@app.route('/logout')
def logout():
    if 'email' in session:
        session.pop('email', None)
        flash('logged out successfull!', 'success')
    
    return redirect(url_for('index'))

@app.route('/change_password',methods=['POST'])
def changepw():
    if 'email' not in session:
        flash('Please log in','error')
        return redirect(url_for('index'))
    
    user = User.query.filter_by(email = session['email']).first()

    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    if not user or not check_password_hash(user.password, current_password):
        flash('Current password is incorrect','error')
        return redirect(url_for('homepage'))

    if new_password != confirm_password:
        flash('New password do not match', 'error')
        return redirect(url_for('homepage'))
    
    user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
    db.session.commit()

    flash('Password successfully changed', 'success')
    return redirect(url_for('homepage'))



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)