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
    
    @classmethod
    def from_scoreboard_data(cls, data, home_or_away):
        opponent = "away" if home_or_away == "home" else "home"
        stats = TeamStats()
        stats.team = data[home_or_away + "_name_abbrev"].upper()
        stats.is_home_team = home_or_away == "home"
        stats.runs = int(data[home_or_away + "_team_runs"])
        stats.runs_allowed = int(data[opponent + "_team_runs"])
        stats.hits = int(data[home_or_away + "_team_hits"])
        stats.hits_allowed = int(data[opponent + "_team_hits"])
        stats.hrs = int(data[home_or_away + "_team_hrs"])
        stats.hrs_allowed = int(data[opponent + "_team_hrs"])
        stats.win = 1 if stats.runs > stats.runs_allowed else 0
        
class Game(db.Model):
    """Models an individual game"""
    gid = db.StringProperty()
    date = db.DateTimeProperty()
    home_stats = db.ReferenceProperty(TeamStats)
    away_stats = db.ReferenceProperty(TeamStats)

    @classmethod
    def from_scoreboard_data(cls, data):
        game = Game()
        
        # id in the scoreboard looks like 2013/04/16/nynmlb-colmlb-1 but in URLs the gid
        # looks like 2013_04_16_nynmlb_colmlb_1, and we store the URL version of the gid
        game.gid = re.sub("[/-]", "_", data["id"])
        game.date = datetime.strptime("%Y/%m/%d", data["original_date"])

        game.home_stats = TeamStats.from_scoreboard_data(data, "home")
        game.away_stats = TeamStats.from_scoreboard_data(data, "away")
        
