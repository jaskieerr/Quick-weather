from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy  # Fixed the typo here
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
    email = db.Column(db.String(255), unique = True ,nullable = False)
    fullname = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    
    user = User.query.filter_by(email=email).first()  # Only filter by email
    
    if user and check_password_hash(user.password, password):  # Verify password
        session['email'] = email
        return render_template('homepage.html')
    else:
        return 'Invalid username or password'
    
@app.route('/register', methods=['POST'])
def register():
    fullname = request.form['fullname']
    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email,).first()

    if user:
        session['email'] = email
        return 'u already have an account'
    else:
    # Hash the password before storing
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(
            fullname=fullname, 
            password=hashed_password,  # Store the hashed password
            email=email
        )
        db.session.add(new_user)
        db.session.commit()
    return f'good job nizar'

if __name__ == '__main__':
    # Create all database tables
    with app.app_context():
        db.create_all()
    app.run(debug=True)