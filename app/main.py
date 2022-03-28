from datetime import datetime
import json
from typing import List
from dataclasses import asdict

from app.config import build_settings
from app.models import MatchModel
from app.scraper import Scraper


def save_to_file(matches: List[MatchModel]):
    timestamp = str(datetime.now())
    matches_as_dicts = [asdict(m) for m in matches]
    with open(f"scraped_products/matches_odds/{timestamp}_matches_odds.json", 'w') as f:
        f.write(json.dumps(matches_as_dicts))


if __name__ == '__main__':
    settings = build_settings()
    scraper = Scraper(settings.scrape_type)
    matches = scraper.scrape_page(settings.url)
    save_to_file(matches)
