import json
import sys

from datetime import date, datetime, timedelta
from urllib2 import urlopen

from models.models import LeagueStats, TeamStats
from models.scraper import Scraper

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
        for game in Scraper.game_data(game_date):
            for team in game_stats(game):
                league.add_stats(team)
    print league
    
    
