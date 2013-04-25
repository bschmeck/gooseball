from datetime import datetime
import re

from google.appengine.ext import db

class TeamStats(db.Model):
    team = db.StringProperty()
    is_home_team = db.BooleanProperty()
    runs = db.IntegerProperty()
    runs_allowed = db.IntegerProperty()
    hits = db.IntegerProperty()
    hits_allowed = db.IntegerProperty()
    hrs = db.IntegerProperty()
    hrs_allowed = db.IntegerProperty()
    win = db.IntegerProperty()

    def __init__(self, home_or_away):
        self.is_home_team = home_or_away == "home"
        
    def populate(self, data):
        (team, opponent) = ("home", "away") if self.is_home_team else ("away", "home")

        self.team = data[team + "_name_abbrev"].upper()
        self.runs = int(data[team + "_team_runs"])
        self.runs_allowed = int(data[opponent + "_team_runs"])
        self.hits = int(data[team + "_team_hits"])
        self.hits_allowed = int(data[opponent + "_team_hits"])
        self.hrs = int(data[team + "_team_hrs"])
        self.hrs_allowed = int(data[opponent + "_team_hrs"])
        self.win = 1 if self.runs > self.runs_allowed else 0
        
class Game(db.Model):
    """Models an individual game"""
    gid = db.StringProperty()
    date = db.DateTimeProperty()
    home_stats = db.ReferenceProperty(TeamStats)
    away_stats = db.ReferenceProperty(TeamStats)

    @classmethod
    def from_scoreboard_data(cls, data):
        # id in the scoreboard looks like 2013/04/16/nynmlb-colmlb-1 but in URLs the gid
        # looks like 2013_04_16_nynmlb_colmlb_1, and we store the URL version of the gid
        gid = re.sub("[/-]", "_", data["id"])

        # If we've already seen this game, we're updating, otherwise we need to create a new game
        game = Game.all().filter("gid = ", gid).get()
        if not game:
            game = Game()        
            game.home_stats = TeamStats("home")
            game.away_stats = TeamStats("away")

        game.date = datetime.strptime("%Y/%m/%d", data["original_date"])

        game.home_stats.populate(data)
        game.away_stats.populate(data)
        
