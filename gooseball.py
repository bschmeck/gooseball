from datetime import datetime, timedelta
import jinja2
import os
import urllib2
import webapp2

from models.db_models import CachedStats, Game
from models.models import LeagueStats, TeamStats
from models.scraper import Scraper

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

def daterange(arr):
        # We are either called with a single date, e.g. 20130401, or a date range 20130401...20130407
        # The way our URL regex works, this shows up as two elements in a list:
        # ["20130401", None] for single dates and ["20130401", "...20130407"] for the range
        # We strip the None (if present) from the list, then join to create a single string
        # Then split on "..." to get a 1 or 2 elt list, and map that to create start and end dates
        daterange = "".join(filter(None, arr))
        dates = map(lambda s: datetime.strptime(s, "%Y%m%d").date(), daterange.split("..."))
        start = dates[0]
        end = dates[1] if len(dates) == 2 else start
        
        return (start, end)

class MainPage(webapp2.RequestHandler):
    def get(self):
        template_values = {'league_stats': LeagueStats()}
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

class Cron(webapp2.RequestHandler):
    def get(self, job):
        if job == "scrape":
            self.scrape()
        elif job == "ping_speedball":
            self.ping("speedball")
        elif job == "ping_lifterapp":
            self.ping("lifterapp")
        elif job == "ping_zrankings":
            self.ping("zrankings")
        elif job == "ping_maple_planner":
            self.ping("maple-planner")
        else:
            self.error(400)

    def ping(self, id):
        try:
            url = {'speedball': "http://speedleague.herokuapp.com/",
                   'lifterapp': "http://lifterapp.herokuapp.com/",
                   'zrankings': "http://zrankings.com",
                   'maple-planner': "http://maple-planner.herokuapp.com/"}[id]
            urllib2.urlopen(url)
        except KeyError:
            pass
        
    def scrape(self):
        scrape_date = datetime.now()
        # Scrape yesterday's games up until 10am Central
        # Dates/times are UTC, which is 5 hours ahead of Central
        if scrape_date.hour < 15:
            scrape_date -= timedelta(days=1)

        for game in Scraper.game_data(scrape_date):
            Game.from_scoreboard_data(game)

        for stat in CachedStats.all():
            stat.delete()
                      
class ScrapeDate(webapp2.RequestHandler):
    def get(self, *a):
        start, end = daterange(a)
        games = []
        while start <= end:
            for game in Scraper.game_data(start):
                games.append(Game.from_scoreboard_data(game))
            start += timedelta(days=1)
            
        for stat in CachedStats.all():
            stat.delete()
        
class Stats(webapp2.RequestHandler):
    def get(self, *a):
        return_type = self.request.get("as").lower() or "text"
        key_name = CachedStats.generate_key("".join(filter(None, a)), return_type)
        cached = CachedStats.get_by_key_name(key_name)

        if not cached:
            cached = CachedStats(key_name = key_name)
            (start, end) = daterange(a)
            league = LeagueStats()
            query = Game.all().filter("date >= ", start).filter("date <= ", end)

            for game in query.run():
                league.add_stats(game.home_stats())
                league.add_stats(game.away_stats())
            if return_type == "json":
                cached.response = league.to_json()
            else:
                template_values = {'league_stats': league}
                template = JINJA_ENVIRONMENT.get_template('index.html')
                cached.response = template.render(template_values)
            cached.put()
            
        if return_type == "json":
            self.response.headers["Content-Type"] = "application/json"
            self.response.write(cached.response)
        else:
            self.response.write(cached.response)
        
        
app = webapp2.WSGIApplication([('/', MainPage),
                               ('/scrape/(\d{8})(\.\.\.\d{8})?/?$', ScrapeDate),
                               ('/cron/(.*)/?$', Cron),
                               ('/stats/(\d{8})(\.\.\.\d{8})?/?$', Stats)],
                              debug=True)
