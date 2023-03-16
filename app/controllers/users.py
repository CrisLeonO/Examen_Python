from app import app
from flask import Flask, render_template, request, redirect, session, flash
from flask_bcrypt import Bcrypt


from app.models.user import User
from app.models.poke import Poke


bcrypt = Bcrypt(app)


@app.route('/main')
def index():
    return render_template('login.html')


# register user
@app.route('/register', methods=['POST'])
def register():
    is_valid = User.validate_user(request.form)

    if not is_valid:
        return redirect("/main")
    print(is_valid)
    new_user = {
        'name': request.form['name'],
        'alias': request.form['alias'],
        'email': request.form['email'],
        'password': request.form['password'],
        'password': bcrypt.generate_password_hash(request.form['password']),
        'birthday': request.form['birthday']
    }

    id = User.save(new_user)
    if not id:
        flash("Email already taken.", "register")
        return redirect('/main')
    session['user_id'] = id
    return redirect('/pokes')


# validate email
@app.route('/login', methods=['POST'])
def login():
    data = {
        'email': request.form['email']
    }
    user = User.get_email(data)
    if not user:
        flash('Invalid email or password', 'login')
        return redirect('/main')

    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Invalid email or password', 'login')
        return redirect('/main')

    session['user_id'] = user.id
    return redirect('/pokes')


@app.route('/pokes')
def pokes():
    if 'user_id' not in session:
        return redirect('/main')
    data = {
        "id": session['user_id']
    }
    # print('here')
    user = User.get__one_user(data)
    users = User.get_all()
    pokes = Poke.get_pokes_of_user(data)
    count_pokes = Poke.count_pokes(data)
    return render_template("pokes.html", user=user, users=users, pokes=pokes, count_pokes=count_pokes)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/main')
