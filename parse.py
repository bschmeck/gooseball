import json
import sys

from datetime import date, datetime, timedelta
from urllib2 import urlopen

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
    home_team = data["home_code"].upper()
    away_team = data["away_code"].upper()
    
    if data["ind"] == 'F':
        fmt_string = "%s,%s,%s,%s,%s"
        home_stats = fmt_string % (home_team, data["home_win"], data["home_loss"], data["home_team_hits"], data["home_team_hr"])
        away_stats = fmt_string % (away_team, data["away_win"], data["away_loss"], data["away_team_hits"], data["away_team_hr"])
    else:
        home_stats = "%s,In Progress" % (home_team)
        away_stats = "%s,In Progress" % (away_team)
    yield home_stats
    yield away_stats

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
    
    
