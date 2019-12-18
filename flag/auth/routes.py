"""Routes for user authentication."""
from flask import redirect, render_template, flash, request, url_for, abort
from flask_login import login_required, logout_user, current_user, login_user
from flask import current_app as app
from werkzeug.security import generate_password_hash
from flag.auth.forms import LoginForm, SignupForm, ForgotForm, ResetPasswordForm, UserForm, ProfileForm
from flag.auth.models import db, User
from flag import login_manager
from flag.auth import bpAuth
from flag.services.mail_api import send_email
import datetime

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
                user.last_login = datetime.datetime.now()
                db.session.commit()
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
                            last_login = datetime.datetime.now(),
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

@bpAuth.route('/users')
def users():
    if not current_user.is_authenticated:
        return redirect(url_for('home'))
    if current_user.userRole != "A":
        abort(401) # unauthorized

    allUsers = User.query.all()
    return render_template('auth/users.html', userList = allUsers)

# @bpAuth.route('/user/<user_id>')
# def user(user_id):
#     if not current_user.is_authenticated:
#         return redirect(url_for('home'))
#     if current_user.userRole != "A":
#         abort(401) # unauthorized

#     user = User.query.filter_by(id=user_id).first()

#     return render_template('auth/user.html', user = user)

@bpAuth.route('/profile/<user_id>', methods=['GET', 'POST'])
def profile(user_id = 0):
    screenMode = 'profile' #came from profile screen
    profile_form = ProfileForm(request.form)
    # POST: Sign user in
    if request.method == 'POST':
        if profile_form.validate():
            # Get Form Fields
            firstName = request.form.get('firstName')
            lastName = request.form.get('lastName')
            website = request.form.get('website')
            phone = request.form.get('phone')
            userId = request.form.get('user_id')
            existing_user = User.query.filter_by(id=userId).first()
            if not existing_user is None:
                existing_user.firstName=firstName
                existing_user.lastName=lastName
                existing_user.website=website
                existing_user.phone=phone
                db.session.commit()
            flash('Profile successfully updated.')
            return redirect(url_for('auth.profile', user_id = userId ))
    else:
        if not current_user.is_authenticated:
            return redirect(url_for('home'))
        if int(user_id) > 0:#check to see if they came from users
            screenMode = 'users'
            if current_user.userRole != "A":
                abort(401) # unauthorized
        else: 
            user_id = current_user.id

        user = User.query.filter_by(id=user_id).first()
        profile_form.firstName.data = user.firstName
        profile_form.lastName.data = user.lastName
        profile_form.phone.data = user.phone or ''
        profile_form.website.data = user.website or ''
        profile_form.user_id.data = user.id
        if user.memberExpireDate == None:
            profile_form.membershipExpiryDate.data = ''
        else:
            profile_form.membershipExpiryDate.data = user.memberExpireDate.strftime('%d-%b-%Y')

    return render_template('auth/profile.html',form=profile_form, screenMode = screenMode)