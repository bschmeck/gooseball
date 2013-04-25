import json

from urllib2 import urlopen

class Scraper:
        
    @classmethod
    def game_data(cls, game_date):
        url = game_date.strftime('http://gdx.mlb.com/components/game/mlb/year_%Y/month_%m/day_%d/miniscoreboard.json')

        data = urlopen(url).read()
        scoreboard = json.loads(data)
        game_arr = scoreboard["data"]["games"]["game"]

        # If there's only one game, it doesn't seem to be in an array.  Force it.
        if type(game_arr) == dict:
            game_arr = [game_arr]
        for game in game_arr:
            yield game
    


