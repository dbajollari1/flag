from flask import Flask, render_template, request, redirect, url_for, flash, session, redirect   
from flag import create_app, db
from flag.dataaccess.homeDAO import getUpcomingEvent, getSiteContents
from flag.events.models import Event
import stripe # pip install stripe
from flag.services.mail_api import send_email

app = create_app()
stripe.api_key="sk_test_qvXYDnAVOqKg0jG4qAHyWuVT00IEP8pWcD"
# You can find your endpoint's secret in your webhook settings
endpoint_secret = 'whsec_olBCMlxUWYldQjQPAYQfjgbTzg0ict3R'

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
  return render_template('donate.html', sid=stripeID)

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
            'images': ['https://arianb1.pythonanywhere.com/static/images/logo.jpg'],
            'amount': int(amount),
            'currency': 'usd',
            'quantity': 1
        }],
        success_url='https://arianb1.pythonanywhere.com/thanks',
        cancel_url='https://arianb1.pythonanywhere.com',
    )   
    return session.id


@app.route('/flag_webhook', methods=['POST'])
def flag_webhook():
    # app.logger.error(request.data.decode("utf-8"), extra={'user': ''})
    try:
      payload = request.data.decode("utf-8")
    except:
      app.logger.error('coud not load payload', extra={'user': ''})

    sig_header = request.headers.get("Stripe-Signature", None) # request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
      event = stripe.Webhook.construct_event(
        payload, sig_header, endpoint_secret
      )
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
    if event.type == 'checkout.session.completed':
        app.logger.error('checkout.session.completed', extra={'user': ''})
    elif event.type == 'payment_intent.succeeded':
        app.logger.error('payment_intent.succeeded', extra={'user': ''})
        # payment_intent = event.data.object # contains a stripe.PaymentIntent
        # handle_payment_intent_succeeded(payment_intent)
    elif event.type == 'payment_method.attached':
        app.logger.error('payment_method.attached', extra={'user': ''})
        # payment_method = event.data.object # contains a stripe.PaymentMethod
        #handle_payment_method_attached(payment_method)
    else:
        # Unexpected event type
        return "Unexpected event type", 400

    app.logger.error(event.data.object.customer_email, extra={'user': ''})
    note= ' '
    try:
      note = event.data.object.display_items.custom.description
    except:
      app.logger.error('coud not get display_items.custom.description', extra={'user': ''})

    cust = stripe.Customer.retrieve(event.data.object.customer) #get cust info

    # email thanking donator
    refNbr = event.data.object.payment_intent
    html_body=render_template('email/thanks_note.html', ref=refNbr)
    send_email('Fort Lee Artist Guild - Donation Received', cust.email, '', html_body)
    # email admin notifying of a donation
    html_body=render_template('email/donation_note.html', message=note, donator=cust.email)
    send_email('Fort Lee Artist Guild - New Donation', app.config['ADMINS'], '', html_body)

    # app.logger.error("Received event: id={id}, type={type}, email={email}".format(id=event.id, type=event.type, email=event.data.object.customer_email))
    return 'OK', 200
