import json
import sys

from datetime import date, datetime, timedelta
from urllib2 import urlopen

class LeagueStats:
    TEAM_CODES = {"ARI","ATL","BAL","BOS","CHC","CIN","CLE","COL","CWS","DET","HOU","KC","LAA","LAD","MIA","MIL","MIN","NYM","NYY","OAK","PHI","PIT","SD","SEA","SF","STL","TB","TEX","TOR","WSH"}
    
    def __init__(self):
        self.teams = {}
        for code in self.TEAM_CODES:
            self.teams[code] = TeamStats(code)
        
    def add_stats(self, stats):
        self.teams[stats.team].add(stats)

    def __str__(self):
        ret = []
        for (code, team) in iter(sorted(self.teams.items())):
            ret.append(str(team))
        return "\n".join(ret)
    
class TeamStats:
    def __init__(self, team):
        self.team = team
        self.hits = 0
        self.hr = 0
        self.win = 0
        self.loss = 0

    def add(self, stats):
        self.hits += stats.hits
        self.hr += stats.hr
        self.win += stats.win
        self.loss += stats.loss
    
    def __str__(self):
        return "%(team)s,%(win)d,%(loss)d,%(hits)d,%(hr)d" % self.__dict__
        
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
    home = TeamStats(data["home_name_abbrev"].upper())
    away = TeamStats(data["away_name_abbrev"].upper())

    if data["ind"] == 'F' or data["ind"] == 'FR':
        home_score = int(data["home_team_runs"])
        away_score = int(data["away_team_runs"])
        home.win = 1 if home_score > away_score else 0
        home.loss = abs(1 - home.win)
        home.hits = int(data["home_team_hits"])
        home.hr = int(data["home_team_hr"])
        away.win = home.loss
        away.loss = home.win
        away.hits = int(data["away_team_hits"])
        away.hr = int(data["away_team_hr"])
    yield home
    yield away

if __name__ == "__main__":
    game_dates = []
    if len(sys.argv) > 1:
        date_str = sys.argv[1]
        if date_str == "yesterday":
            game_dates.append(date.today() - timedelta(days=1))
        elif date_str == "week":
            dte = date.today()
            cur_day = dte.weekday()
            if cur_day == 0:
                # If today is Monday, assume we want last week's stats
                dte -= timedelta(days=1)
                cur_day = dte.weekday()
            while cur_day >= 0:
                game_dates.append(dte)
                dte -= timedelta(days=1)
                cur_day -= 1
        else:
            game_dates.append(datetime.strptime(date_str, "%Y%m%d"))

    if len(game_dates) == 0:
        game_dates.append(date.today())

    league = LeagueStats()
    for game_date in game_dates:
        for game in game_data(game_date):
            for team in game_stats(game):
                league.add_stats(team)
    print league
    
    
