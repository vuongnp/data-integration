from .db import db

class Movie(db.Document):
    name = db.StringField(required=True)
    casts = db.ListField(db.StringField())
    genres = db.ListField(db.StringField())
    links = db.ListField(db.StringField())
    image = db.StringField()
    imdb = db.FloatField()

    meta = {'indexes': [
        {'fields': ['$name', "$casts", "$genres"],
         'default_language': 'english',
        #  'weights': {'title': 10, 'content': 2}
        }
    ]}