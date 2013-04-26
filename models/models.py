import json

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
        for (code, team) in self.teams_iter():
            ret.append(str(team))
        return "\n".join(ret)

    def teams_iter(self):
        return iter(sorted(self.teams.items()))

    def to_json(self):
        ret = {}
        for (code, team) in self.teams_iter():
            ret[code] = team.__dict__
        return json.dumps(ret)
        
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
