import webapp2
import jinja2
import os

from google.appengine.ext import db
from parse import LeagueStats, TeamStats

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

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
      template_values = {'league_stats': LeagueStats()}
      template = JINJA_ENVIRONMENT.get_template('index.html')
      self.response.write(template.render(template_values))

class Stats(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Weekly stats')
        
app = webapp2.WSGIApplication([('/', MainPage),
                               ('/stats', Stats)],
                              debug=True)
