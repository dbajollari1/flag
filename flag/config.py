import os

class Config(object):
    SECRET_KEY = 'vfr'
    ADMINS = 'dbajollari1@yahoo.com'
    MJ_APIKEY_PUBLIC = '077fc21857d31f1f416fbf1ab7477164'
    MJ_APIKEY_PRIVATE = '03caddedf8edb44156d03585242e359a'
    MJ_EMAIL = 'fortleeartists@gmail.com'
    SQLITE_PATH = 'db/flag.sqlite'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../db/flag.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ST_PBK = 'pk_test_DCZF4C9gpgFyjNJQYGOYiGmx00aE0ErF94'
    ST_PVK = 'sk_test_8OGNYcJKB0TWieGnYFTlrmd700h8t0ovw6'
    ST_WEBHK = 'whsec_wV0dI8let4lPZvO68yKA9XMhjwoK7ydE'
    HOME_PAGE = 'http://127.0.0.1:5000/home'
    MEMBERSHIP_SUCCESS_URL = 'http://127.0.0.1:5000/membership?paid=Y'
    MEMBERSHIP_AMT = 30
    MEMBERSHIP_DURATION = 1
    SITE_LOGO = 'http://127.0.0.1:5000/static/images/logo1.png'
    DONATE_SUCCESS_URL = 'http://127.0.0.1:5000/thanks'
    SUPPORT = 'dbajollari1@yahoo.com'