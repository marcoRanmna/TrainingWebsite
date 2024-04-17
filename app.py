import os
from flask import Flask, request, render_template, redirect
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


from logic import calc_bmr
from config import ProductionConfig, DevelopmentConfig
from models.user import db, User

app = Flask(__name__)
if os.getenv('RUNENVIRONMENT') == "Production":
    app.config.from_object(ProductionConfig())
else:
    app.config.from_object(DevelopmentConfig())

#hello world

db.init_app(app)

def create_tables():
    with app.app_context():
        db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calorie-calculator', methods=['GET', 'POST'])
def calorie_calculator():
      if request.method == 'POST':
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        age = int(request.form['age'])
        gender = request.form['gender']
        training_difficulty = request.form['training_difficulty']

        bmr = calc_bmr.calculate_bmr(weight, height, age, gender, training_difficulty)
        return render_template('calorie_calculator_result.html', bmr=bmr)
      else:
        return render_template('calorie_calculator_form.html')

@app.route('/training-programs')
def training_programs():
    return render_template('training_programs.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect('/')
        else:
            return 'Invalid username or password', 401

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        try:
            new_user = User(username=username, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect('/login')
        except IntegrityError:
            db.session.rollback()
            return 'Username or email already exists. Please choose another.', 409

  return render_template('register.html')

if __name__ == '__main__':
    create_tables()
    app.run()