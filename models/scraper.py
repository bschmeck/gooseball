import json

from urllib2 import urlopen

class Scraper:
    @classmethod
    def game_data(cls, game_date):
        year = game_date.strftime('%Y')
        month = game_date.strftime('%m')
        day = game_date.strftime('%d')

        game_data(year, month, day)

    @classmethod
    def game_data(cls, year, month, day):
        url = 'http://gdx.mlb.com/components/game/mlb/year_%(year)s/month_%(month)s/day_%(day)s/miniscoreboard.json' % locals()

        data = urlopen(url).read()
        scoreboard = json.loads(data)
        game_arr = scoreboard["data"]["games"]["game"]

        # If there's only one game, it doesn't seem to be in an array.  Force it.
        if type(game_arr) == dict:
            game_arr = [game_arr]
        for game in game_arr:
            yield game
    


