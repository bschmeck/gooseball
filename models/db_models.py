from datetime import datetime
import re

from google.appengine.ext import db

class Game(db.Model):
    """Models an individual game"""
    date = db.DateProperty()
    home_team = db.StringProperty()
    away_team = db.StringProperty()
    home_runs = db.IntegerProperty()
    away_runs = db.IntegerProperty()
    home_hits = db.IntegerProperty()
    away_hits = db.IntegerProperty()
    home_hrs = db.IntegerProperty()
    away_hrs = db.IntegerProperty()
    home_win = db.IntegerProperty()
    away_win = db.IntegerProperty()
    
    @classmethod
    def from_scoreboard_data(cls, data):
        # id in the scoreboard looks like 2013/04/16/nynmlb-colmlb-1 but in URLs the gid
        # looks like 2013_04_16_nynmlb_colmlb_1, and we store the URL version of the gid
        gid = re.sub("[/-]", "_", data["id"])

        # If we've already seen this game, we'll just overwrite it
        game = Game(key_name=gid)
        game.date = datetime.strptime(data["original_date"], "%Y/%m/%d").date()
        game.home_team = data["home_name_abbrev"].upper()
        game.away_team = data["away_name_abbrev"].upper()
        game.home_runs = int(data["home_team_runs"])
        game.away_runs = int(data["away_team_runs"])
        game.home_hits = int(data["home_team_hits"])
        game.away_hits = int(data["away_team_hits"])
        game.home_hrs = int(data["home_team_hr"])
        game.away_hrs = int(data["away_team_hr"])
        game.home_win = 1 if game.home_runs > game.away_runs else 0
        game.away_win = abs(1 - game.home_win)

        game.put()
