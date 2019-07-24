from mailjet_rest import Client
from flask import current_app as app

def send_email(subject, sender, recipients, text_body, html_body):
    fromName = "Fort Lee Artist Guild"
    fromEmail = "arianb1@hotmail.com" #has to valid email registered in mailjet
    toEmail = "abajollari@yahoo.com"
    api_key = app.config['MJ_APIKEY_PUBLIC']
    api_secret = app.config['MJ_APIKEY_PRIVATE']
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    data = {
    'Messages': [
                    {
                            "From": {
                                    "Email": fromEmail,
                                    "Name": fromName
                            },
                            "To": [
                                    {
                                            "Email": toEmail,
                                            "Name": "Arian"
                                    },
                                    {
                                            "Email": "dbajollari1@gmail.com",
                                            "Name": "David"
                                    }
                            ],
                            "Subject": subject,
                            "TextPart": text_body,
                            "HTMLPart": html_body
                    }
            ]
    }
    result = mailjet.send.create(data=data)
    print(result.status_code)
    print(result.json())