import webapp2
import jinja2
import os

from models.db_models import Game
from models.models import LeagueStats, TeamStats

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

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
