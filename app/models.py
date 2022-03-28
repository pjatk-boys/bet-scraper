import dataclasses
from datetime import datetime


@dataclasses.dataclass
class TeamModel:
    name: str
    odds: str
    bet_amount: str


@dataclasses.dataclass
class MatchModel:
    # scrape_timestamp = datetime.datetime.now() #todo
    meeting_minute: datetime.time
    league: str
    first_team: TeamModel
    second_team: TeamModel
    draw_odds: int
    draw_amount: str
    current_score: str
