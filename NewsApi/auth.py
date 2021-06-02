import operator

from flask import request, make_response, jsonify
from NewsApi.app import app, db
from NewsApi import models


@app.route('/register', methods=['POST'])
def sign_up():
    new_user = models.User(username=request.json['username'],
                           email=request.json['email'])
    if not new_user:
        error = 'Username is required.'
    elif not password:
        error = 'Password is required.'
    elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
    ).fetchone() is not None:
        error = f"User {username} is already registered."
    db.session.add(new_user)
    db.session.commit()
    return make_response(jsonify(response='OK'), 201)



@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = f"User {username} is already registered."

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')