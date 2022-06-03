from flask import Flask
import os

# папка для сохранения загруженных файлов
UPLOAD_FOLDER = '/home/magomedali/Рабочий стол/my_diplom/app/static/files'

# расширения файлов, которые разрешено загружать
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'xls'}

app = Flask(__name__)
# конфигурируем
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'some random string'
app.config['JSON_AS_ASCII'] = False


from flask_pymongo import PyMongo

mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/poletinf")
db = mongodb_client.db


from flask_mongoengine import MongoEngine
app.config['MONGODB_SETTINGS'] = {
    'db':'poletinf',
    'host':'localhost',
    'port':'27017'
}

app.config['MONGODB_SETTINGS'] = {
    'host':'mongodb://localhost/fly'
}


db2 = MongoEngine(app)