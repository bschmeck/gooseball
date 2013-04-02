import json
import sys

from datetime import date, datetime, timedelta
from urllib2 import urlopen

class TeamStats:
    def __init__(self, team):
        self.team = team
        self.hits = 0
        self.hr = 0
        self.win = 0
        self.loss = 0

    def final(self):
        return self.win + self.loss > 0
    
    def __str__(self):
        if self.final():
            fmt_string = "%s,%d,%d,%d,%d"
            return fmt_string % (self.team, self.win, self.loss, self.hits, self.hr)
        else:
            return "%s,In Progress" % (self.team)
        
def game_data(game_date):
    year = game_date.strftime('%Y')
    month = game_date.strftime('%m')
    day = game_date.strftime('%d')
    url = 'http://gdx.mlb.com/components/game/mlb/year_%(year)s/month_%(month)s/day_%(day)s/miniscoreboard.json' % locals()

    data = urlopen(url).read()
    scoreboard = json.loads(data)
    game_arr = scoreboard["data"]["games"]["game"]

    # If there's only one game, it doesn't seem to be in an array.  Force it.
    if type(game_arr) == dict:
        game_arr = [game_arr]
    for game in game_arr:
        yield game

def game_stats(data):
    home = TeamStats(data["home_code"].upper())
    away = TeamStats(data["away_code"].upper())
    
    if data["ind"] == 'F':
        home.win = int(data["home_win"])
        home.loss = int(data["home_loss"])
        home.hits = int(data["home_team_hits"])
        home.hr = int(data["home_team_hr"])
        away.win = int(data["away_win"])
        away.loss = int(data["away_loss"])
        away.hits = int(data["away_team_hits"])
        away.hr = int(data["away_team_hr"])
    yield home
    yield away

if __name__ == "__main__":
    game_date = None
    if len(sys.argv) > 1:
        date_str = sys.argv[1]
        if date_str == "yesterday":
            game_date = date.today() - timedelta(days=1)
        else:
            game_date = datetime.strptime(date_str, "%Y%m%d")
    if not game_date:
        game_date = date.today()

    for game in game_data(game_date):
        for team in game_stats(game):
            print team
    
    
