
class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost:3306/demo'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY ='abc123'
    TWEET_PER_PAGE =3

    MAIL_DEFAULT_SENDER ='noreply@t.com'
    MAIL_SERVER = ''
    MAIL_PORT =''
    MAIL_USE_TLS =1
    MAIL_USERNAME =''
    MAIL_PASSWORD =''