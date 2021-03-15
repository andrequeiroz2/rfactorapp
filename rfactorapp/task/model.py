from rfactorapp.database import db
import datetime


class Tasks(db.Document):
    name = db.StringField(minlength=3, max_length=30, required=True, unique=True)
    description = db.StringField(minlength=3, max_length=200, required=True)
    status = db.StringField(default='open', required=True)
    createtad = db.DateTimeField(default=datetime.datetime.utcnow)




