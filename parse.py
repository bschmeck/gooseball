import json
import sys

from datetime import date, datetime
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
    fmt_string = "%s,%s,%s,%s,%s"
    yield fmt_string % (data["home_code"].upper(), data["home_win"], data["home_loss"], data["home_team_hits"], data["home_team_hr"])
    yield fmt_string % (data["away_code"].upper(), data["away_win"], data["away_loss"], data["away_team_hits"], data["away_team_hr"])

if __name__ == "__main__":
    game_date = None
    if len(sys.argv) > 1:
        date_str = sys.argv[1]
        game_date = datetime.strptime(date_str, "%Y%m%d")
    if not game_date:
        game_date = date.today()

    for game in game_data(game_date):
        for team in game_stats(game):
            print team
    
    
