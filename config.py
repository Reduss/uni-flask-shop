class Config():
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root@localhost/sdb_shop'
    MONGO_URI = 'mongodb://localhost:27017'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STATIC_FOLDER = 'static'
    SECRET_KEY = '123'