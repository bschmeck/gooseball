import webapp2

from google.appengine.ext import db

class Game(db.Model):
    """Models an individual game"""
    home_team = db.StringProperty()
    away_team = db.StringProperty()
    home_runs = db.IntegerProperty()
    away_runs = db.IntegerProperty()
    home_hits = db.IntegerProperty()
    away_hits = db.IntegerProperty()
    home_hrs = db.IntegerProperty()
    away_hrs = db.IntegerProperty()
    date = db.DateTimeProperty()

class MainPage(webapp2.RequestHandler):
  def get(self):
      self.response.headers['Content-Type'] = 'text/plain'
      self.response.write('Hello, webapp2 World!!!')

class Stats(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Weekly stats')
        
app = webapp2.WSGIApplication([('/', MainPage),
                               ('/stats', Stats)],
                              debug=True)
