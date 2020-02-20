from flask import render_template, redirect, url_for, request, flash, redirect
from flag.membership import bpMembership
from flask_login import login_required, current_user
from flag.auth.models import db, User
from flask import current_app as app
from datetime import date, timedelta, datetime
import stripe # pip install stripe

@bpMembership.route('/membership')
@login_required
def membership():
    paid = request.args.get('paid')
    if paid == 'Y': #redirected from stripe after payment as been made (see success_url below)
        # extendMembership('aa@aa.com') ##### To test from local code  only
        return render_template('membership/membership.html', paid='Y')

    amt = int(app.config['MEMBERSHIP_AMT'])
    stripeID = createSession(amt*100)  # stripe values are in cents
    stripe_pk = app.config['ST_PBK'] # stripe public key
    return render_template('membership/membership.html', sid=stripeID, st_pk=stripe_pk, amt='${:,.2f}'.format(amt))


def createSession(amt):
    stripe.api_key = app.config['ST_PVK'] # stripe private key
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        customer_email = current_user.email,
        submit_type = 'pay', # 'donate' or 'auto'          
        line_items=[{
            'name': 'Membership Fee',
            'description': 'Annual Membership Fee',
            'images': [app.config['SITE_LOGO']],
            'amount': int(amt),
            'currency': 'usd',
            'quantity': 1
        }],
        success_url=app.config['MEMBERSHIP_SUCCESS_URL'],
        cancel_url=app.config['HOME_PAGE']
    )   
    return session.id

# function is called from stripe webhook (see in app.py) after payment received
def extendMembership(userEmail):
    existing_user = User.query.filter_by(email=userEmail).first()
    membershipDays = int(app.config['MEMBERSHIP_DURATION'])*365 + 1
    if not existing_user is None:  #found user who made the payment
        if existing_user.memberStartDate is None: #new membership
            existing_user.memberStartDate = date.today()
            existing_user.memberExpireDate = date.today() + timedelta(days = membershipDays)
        else: #use expiry date if memmbership not yet expired
            if existing_user.memberExpireDate > datetime.datetime.now():
                existing_user.memberStartDate = existing_user.memberExpireDate
                existing_user.memberExpireDate = existing_user.memberStartDate  + timedelta(days = membershipDays)
            else:
                existing_user.memberStartDate = date.today()
                existing_user.memberExpireDate = date.today() + timedelta(days = membershipDays)
        existing_user.membershipStatus = "A" # Active membership
        existing_user.updatedMembership = userEmail
        db.session.commit()


    
