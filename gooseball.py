from datetime import datetime, timedelta
import jinja2
import os
import webapp2

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

class Stats(webapp2.RequestHandler):
    def get(self, daterange):
        (start, end) = map(lambda s: datetime.strptime(s, "%Y%m%d").date(), daterange.split("..."))
        league = LeagueStats()
        query = Game.all().filter("date >= ", start).filter("date <= ", end)

        for game in query.run():
            league.add_stats(game.home_stats())
            league.add_stats(game.away_stats())
        template_values = {'league_stats': league}
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))
        
        
app = webapp2.WSGIApplication([('/', MainPage),
                               ('/scrape/(\d{4})/(\d{2})/(\d{2})/?$', ScrapeDate),
                               ('/stats/(\d{8}\.\.\.\d{8})/?$', Stats)],
                              debug=True)
