import functools
from flask import (
    Blueprint, flash, g, render_template, request, url_for, session, redirect
)
from werkzeug.security import check_password_hash
from main.db import get_db
bp = Blueprint('auth', __name__, url_prefix='/auth')

#Login Parents
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db, c = get_db()
        error = None
        c.execute(
            'select * from user where username = %s', (username,)
        )
        user = c.fetchone()

        if user is None:
            error = 'Usuario y/o contrasena invalida'
        elif not check_password_hash(user['password'], password):
            error = 'Usuario y/o contrasena invalida'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('system.index_enroll'))
        flash(error)
    return render_template('system/auth/login.html')

#------------------------------------------------------
#Login Autentificacion Parents Protege Endpoints
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        db, c = get_db()
        c.execute(
            'select * from user where id = %s', (user_id,)
        )
        g.user = c.fetchone()

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    
    return wrapped_view

#------------------------------------------------------
#Logout
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


