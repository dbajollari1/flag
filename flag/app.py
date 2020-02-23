from flask import Flask, render_template, request, redirect, url_for, flash, session, redirect   
from flag import create_app, db
from flag.dataaccess.homeDAO import getUpcomingEvent, getSiteContents
from flag.events.models import Event
import stripe # pip install stripe
from flag.services.mail_api import send_email
from flag.membership.routes import extendMembership

app = create_app()
stripe.api_key = app.config['ST_PVK'] # stripe private key

@app.route('/')
@app.route('/home')
def home():
    try:
        event = getUpcomingEvent()
        siteContents = getSiteContents()
        return render_template('index.html', event = event, siteContentList = siteContents)
    except Exception as e:
        app.logger.error(str(e), extra={'user': ''})
        return redirect(url_for('errors.error'))

@app.route('/donate', methods=['POST'])
def donate():
  amt = 0
  amtEntered=request.form['amount']
  message=request.form['message'] + ' '
  try:
      amt = float(amtEntered)
      if amt < 5 or amt > 1000:
        flash('Amount must be between $5 and $1000')
        return redirect(url_for('home'))        
  except ValueError:
      flash('Amount must be between $5 and $1000')
      return redirect(url_for('home'))

  stripeID = createSession(amt*100, message)  # stripe values are in cents
  stripe_pk = app.config['ST_PBK'] # stripe public key
  return render_template('donate.html', sid=stripeID, st_pk=stripe_pk)

@app.route('/thanks')
def thanks():
  return render_template('thanks.html')

def createSession(amount, message):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        customer_email = None,
        submit_type = 'donate', # 'pay' or 'auto'          customer_email= 'abajollari@yahoo.com',
        line_items=[{
            'name': 'Donation', #'Membership Fee',
            'description': message, #'Annual Membership Fee',
            'images': [app.config['SITE_LOGO']],
            'amount': int(amount),
            'currency': 'usd',
            'quantity': 1
        }],
        success_url = app.config['DONATE_SUCCESS_URL'],
        cancel_url = app.config['HOME_PAGE'],
    )   
    return session.id


@app.route('/flag_webhook', methods=['POST'])
def flag_webhook():
  try:
    # app.logger.error(request.data.decode("utf-8"), extra={'user': ''})
    try:
      payload = request.data.decode("utf-8")
    except:
      app.logger.error('coud not load payload', extra={'user': ''})
      return "error", 400

    sig_header = request.headers.get("Stripe-Signature", None) # request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:   
      endpoint_secret = app.config['ST_WEBHK'] # You can find your endpoint's secret in your webhook settings
      event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
      # Invalid payload
      app.logger.error('Invalid payload' + str(e), extra={'user': ''})
      return "Value Error", 400
    except stripe.error.SignatureVerificationError as es:
      app.logger.error('Bad signature' + str(es), extra={'user': ''})
      return "Bad signature", 400
    except Exception as ex:
      app.logger.error('cound not create event' + str(ex), extra={'user': ''})
      return "error", 400

    # Handle the event
    if event.type != 'checkout.session.completed':  #event configured in sripe webhook
      return "Unexpected event type", 400

    refNbr = event.data.object.payment_intent

    if event.data.object.submit_type == 'donate': #donation - email thanking donator

      donatorMessage= ' '
      try:
        donatorMessage = event.data.object.display_items[0].custom.description
      except:
        app.logger.error('coud not get display_items.custom.description', extra={'user': ''})

      cust = stripe.Customer.retrieve(event.data.object.customer) #get cust info
      # Email donator
      html_body=render_template('email/donation_thanks.html', ref=refNbr)
      send_email('Fort Lee Artist Guild - Donation Received', cust.email, '', html_body)
      # Email admin notifying of a donation
      html_body=render_template('email/donation_received.html', message=donatorMessage, donator=cust.email)
      send_email('Fort Lee Artist Guild - New Donation', app.config['ADMINS'], '', html_body)

    else: #submit_type == 'pay' - membership payment

      userEmail = event.data.object.customer_email
      extendMembership(userEmail) #update user's membership
      # Notify user via email
      html_body=render_template('email/membership_thanks.html', ref=refNbr)
      send_email('Fort Lee Artist Guild - Membership payment', userEmail, '', html_body)
      # Nofify admin
      html_body=render_template('email/membership_received.html', message='', member=userEmail)
      send_email('Fort Lee Artist Guild - Membership payment received', app.config['ADMINS'], '', html_body)

    # app.logger.error("Received event: id={id}, type={type}, email={email}".format(id=event.id, type=event.type, email=event.data.object.customer_email))
    return 'OK', 200
  except Exception as e:
    app.logger.error('weeb hook failed' + str(e), extra={'user': ''})
    return "error", 400
