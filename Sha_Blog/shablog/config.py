# import os

class Config:
    # secret key for aplication, so nobody can modify form data
    # best to use environment variable
    SECRET_KEY = '4cb195a017b7d117311173f6d1635375'
    # best to use environment variable
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'

    MAIL_SERVER = 'smtp.mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USERNAME = '122d165e913133'
    MAIL_PASSWORD = 'c207bda3a5272a'
    MAIL_USE_TLS = True

    # as environment variable
    # MAIL_USERNAME = os.environ.get('EMAIL_USERNAME')


class Constants:
    DEFAULT_PROFILE_PICTURE = 'default.jpg'
    PATH_PROFILE_PICTURE = 'static/profile_pics'

    LOGIN_VIEW = 'users.login'
    LOGIN_MESSAGE_CATEGORY = 'info'
