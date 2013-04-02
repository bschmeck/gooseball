import json

from datetime import date
from urllib2 import urlopen

def game_data(game_date):
    year = game_date.strftime('%Y')
    month = game_date.strftime('%m')
    day = game_date.strftime('%d')
    url = 'http://gdx.mlb.com/components/game/mlb/year_%(year)s/month_%(month)s/day_%(day)s/miniscoreboard.json' % locals()

    data = urlopen(url).read()
    scoreboard = json.loads(data)

    for game in scoreboard["data"]["games"]["game"]:
        yield game

def game_stats(data):
    fmt_string = "%s,%s,%s,%s,%s"
    yield fmt_string % (data["home_code"].upper(), data["home_win"], data["home_loss"], data["home_team_hits"], data["home_team_hr"])
    yield fmt_string % (data["away_code"].upper(), data["away_win"], data["away_loss"], data["away_team_hits"], data["away_team_hr"])

if __name__ == "__main__":
    for game in game_data(date.today()):
        for team in game_stats(game):
            print team
    
    
