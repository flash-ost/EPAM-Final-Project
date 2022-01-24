from forms import LoginForm, RegistrationForm
from service import check_credentials, register_user
from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user


bp = Blueprint('auth', __name__)

@bp.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""
    # Redirect to search page if user is authenticated
    if current_user.is_authenticated:
        return redirect(url_for('search.search'))

    # Validate credentials and log user in
    form = LoginForm()
    if form.validate_on_submit():
        user = check_credentials(form.username.data, form.password.data)
        if not user:
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('.login'))
        login_user(user, remember=form.remember_me.data)    
        return redirect(url_for('search.search'))

    return render_template('login.html', title='Sign In', form=form)


@bp.route('/logout')
def logout():
    """Log user out."""
    logout_user()
    return redirect(url_for('auth.login'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Register user."""
    # Redirect to search page if user is authenticated
    if current_user.is_authenticated:
        return redirect(url_for('search.search'))

    # Validate input and register user  
    form = RegistrationForm()
    if form.validate_on_submit():
        if register_user(form.username.data, form.password.data):
            flash('Congratulations, you have been registered! Now you can log in', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Something went wrong, please try again.', 'danger')
               
    return render_template('register.html', title='Register', form=form)