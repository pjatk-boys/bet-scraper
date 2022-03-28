from dataclasses import dataclass
from dacite import from_dict
import json


@dataclass
class Settings:
    url: str
    scrape_type: str


def build_settings() -> Settings:
    with open('app/config.json', 'r') as f:
        data = json.loads(f.read())
        settings = from_dict(data_class=Settings, data=data)
        return settings
