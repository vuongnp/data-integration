from .db import db

class General(db.Document):
    title = db.StringField(required=True)
    actors = db.ListField(db.StringField())
    directors = db.ListField(db.StringField())
    genres = db.ListField(db.StringField())
    urls = db.ListField(db.StringField())
    image = db.StringField()
    rating = db.FloatField()
    year = db.FloatField()
    description = db.StringField()
    duration = db.StringField()

    meta = {'indexes': [
        {'fields': ['$title', "$directors", "$actors", "$genres"],
         'default_language': 'english',
        #  'weights': {'title': 10, 'content': 2}
        }
    ]}