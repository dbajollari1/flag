"""Routes for user authentication."""
from flask import redirect, render_template, flash, Blueprint, request, url_for
from flask_login import login_required, logout_user, current_user, login_user
from flask import current_app as app
from werkzeug.security import generate_password_hash
from flag.auth.forms import LoginForm, SignupForm, ForgotForm, ResetPasswordForm
from flag.auth.models import db, User
from flag import login_manager
from flag.auth import bpAuth
from flag.services.mail_api import send_email

@bpAuth.route('/login', methods=['GET', 'POST'])
def login():
    """User login page."""
    # Bypass Login screen if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    print(request.args.get('next'))
    login_form = LoginForm(request.form)
    # POST: Create user and redirect them to the app
    if request.method == 'POST':
        if login_form.validate() == False:    
            return render_template('auth/login.html',form=login_form)
        # Get Form Fields
        email = request.form.get('email')
        password = request.form.get('password')
        # Validate Login Attempt
        user = User.query.filter_by(email=email).first()
        if user:
            if user.check_password(password=password):
                login_user(user, remember=login_form.remember_me.data)
                next = request.args.get('next')
                return redirect(next or url_for('home')) # SUCCESSFULL LOGIN
        flash('Invalid username or password')

    # GET: Serve Log-in page
    return render_template('auth/login.html',form=login_form)


@bpAuth.route('/signup', methods=['GET', 'POST'])
def signup():
    """User sign-up page."""
    signup_form = SignupForm(request.form)
    # POST: Sign user in
    if request.method == 'POST':
        if signup_form.validate():
            # Get Form Fields
            firstName = request.form.get('firstName')
            lastName = request.form.get('lastName')
            email = request.form.get('email')
            password = request.form.get('password')
            phone = request.form.get('phone')
            existing_user = User.query.filter_by(email=email).first()
            if existing_user is None:
                user = User(firstName=firstName,
                            lastName=lastName,
                            email=email,
                            password=generate_password_hash(password, method='sha256'),
                            phone=phone,
                            userRole='U')
                db.session.add(user)
                db.session.commit()
                login_user(user)
                return redirect(url_for('home'))
            flash('A user already exists with that email address.')
            return redirect(url_for('auth.signup'))
    # GET: Serve Sign-up page
    return render_template('auth/signup.html',form=signup_form)


@bpAuth.route("/logout")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('home'))


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth.login', next=request.path))

@bpAuth.route("/forgot", methods=['GET', 'POST'])
def forgot():
    forgot_form = ForgotForm(request.form)
    linkSent = 'N'
    if request.method == 'POST':
        if forgot_form.validate():
            linkSent = 'Y' # tell user link is sent even if not a valid OR unregistered user email
            email = request.form.get('email')
            existing_user = User.query.filter_by(email=email).first()
            if not existing_user is None: #user exists, send reset link
                token = existing_user.get_reset_password_token()
                text_body=render_template('auth/reset_pwd_lnk.txt', user=existing_user, token=token)
                send_email('Fort Lee Artist Guild - Reset Password', existing_user.email, text_body,'')
    return render_template('auth/forgot.html',form=forgot_form, linkSent=linkSent)


@bpAuth.route('/reset_pwd/<token>', methods=['GET', 'POST'])
def reset_pwd(token):
    try:
        if current_user.is_authenticated:
            return redirect(url_for('home'))

        user = User.verify_reset_password_token(token)
        if not user: #invalid token
            return redirect(url_for('home'))
        resetForm = ResetPasswordForm(request.form)

        if request.method == 'POST':
            if resetForm.validate():
                user.set_password(resetForm.password.data)
                db.session.commit()
                flash('Your password has been reset.')
                return redirect(url_for('home'))
        return render_template('auth/reset_pwd.html', form=resetForm)
    except Exception as e:
        app.logger.error(str(e), extra={'user': ''})
        return redirect(url_for('errors.error'))