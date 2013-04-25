import webapp2
import jinja2
import os

from models.db_models import Game
from models.models import LeagueStats, TeamStats
from models.scraper import Scraper

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainPage(webapp2.RequestHandler):
    def get(self):
        template_values = {'league_stats': LeagueStats()}
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

class ScrapeDate(webapp2.RequestHandler):
    def get(self, *a):
        year = a[0]
        month = a[1]
        day = a[2]

        games = []
        for game in Scraper.game_data(year, month, day):
            games.append(Game.from_scoreboard_data(game))
        print len(games)
        
app = webapp2.WSGIApplication([('/', MainPage),
                               ('/scrape/(\d{4})/(\d{2})/(\d{2})/?$', ScrapeDate)],
                              debug=True)
