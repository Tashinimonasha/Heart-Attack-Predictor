from flask import Flask, render_template, request,redirect, session, url_for, flash
import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jfhfvhkrjdsls12k4jfhrhkgh43kfh2221'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Dineth2021#@localhost/heart_attacker'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False)

# Load Random Forest model and scaler
model = joblib.load('Random_Forest_model.pkl')
scaler = joblib.load('scaler.pkl')
columns = joblib.load('columns.pkl')

# Function to preprocess input data
def preprocess_input(input_data):
    input_df = pd.DataFrame([input_data], columns=columns)
    input_df = scaler.transform(input_df)
    return input_df

# Home page
@app.route('/')
def home():
    return render_template('home.html')

# Prediction page
@app.route('/predictor')
def predictor():
    if 'user_id' not in session:
        flash('You need to login to access the predictor.', 'warning')
        return redirect(url_for('login'))
    return render_template('predictor.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id  
            flash('Login successful.', 'success')
            return redirect(url_for('predictor'))
        else:
            flash('Login unsuccessful. Check your username and password.', 'danger')
            # return redirect(url_for('login'))

    return render_template('login.html')

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            # return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. Please login.', 'success')
            # return redirect(url_for('login'))
        except:
            flash('Error: Username or email already exists.', 'danger')
            # return redirect(url_for('register'))

    return render_template('register.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('user_id', None) 
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# About page
@app.route('/about')
def about():
    return render_template('about.html')



# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        input_data = request.form.to_dict()
        input_data = [float(input_data[col]) for col in columns]
        input_df = preprocess_input(input_data)
        prediction = model.predict(input_df)[0]
        if prediction == 0:
            result = "Low risk of heart attack"
        else:
            result = "High risk of heart attack"
        return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
