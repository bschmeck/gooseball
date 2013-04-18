from google.appengine.ext import db

class Game(db.Model):
    """Models an individual game"""
    gid = db.StringProperty()
    team = db.StringProperty()
    runs = db.IntegerProperty()
    runs_allowed = db.IntegerProperty()
    hits = db.IntegerProperty()
    hits_allowed = db.IntegerProperty()
    hrs = db.IntegerProperty()
    hrs_allowed = db.IntegerProperty()
    date = db.DateTimeProperty()
