from time import sleep
from typing import List

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver

from selenium.webdriver.support.select import Select

from app.models import MatchModel, TeamModel


class Scraper:
    def __init__(self, dropdown_option):
        self.dropdown_option = dropdown_option

    def scrape_page(self, url: str):
        driver = self._build_driver(url)
        dropdown = self._get_dropdown(driver)
        dropdown_options = [o.get_attribute('value') for o in dropdown.options]
        self._validate_option_availability(dropdown_options)
        self._select_dropdown_option(dropdown)
        matches_div = self._get_matches_list(driver)
        matches = self._scrape_match_odds(matches_div)
        driver.close()
        return matches

    def _get_dropdown(self, driver) -> Select:
        dropdown = driver.find_element_by_id('refresh-dropdown')
        dropdown_select = Select(dropdown)
        return dropdown_select

    @staticmethod
    def _is_odds(hour: str) -> bool:
        if ":" not in hour:
            return True
        return False

    def _scrape_match_odds(self, match_list_elems: List) -> List[MatchModel]:
        sleep(3)
        matches = []
        print(f"number of matches list: {len(match_list_elems)}")

        for match in match_list_elems:
            try:

                match_info = match.text
                match_info_list = match_info.split("\n")

                if not self._is_odds(match_info_list[0]):
                    print("this match is not odds!")
                    continue
                else:
                    print(f"this match is odds: {match.text}")
                meeting_minute = match_info_list[0]
                score = match_info_list[1]
                league = match_info_list[2]
                teams = match_info_list[3]
                first_team_bet_amount = match_info_list[4]
                first_team_odds = match_info_list[6]
                draw_amount = match_info_list[7]
                draw_odds = match_info_list[9]
                second_team_bet_amount = match_info_list[10]
                second_team_odds = match_info_list[12]

                first_team_name = teams.split("-")[0].strip()
                second_team_name = teams.split("-")[1].strip()

                first_team = TeamModel(name=first_team_name, odds=first_team_odds, bet_amount=first_team_bet_amount)
                second_team = TeamModel(name=second_team_name, odds=second_team_odds, bet_amount=second_team_bet_amount)
                match_model = MatchModel(meeting_minute=meeting_minute, league=league, first_team=first_team,
                                         second_team=second_team, draw_odds=draw_odds, draw_amount=draw_amount,
                                         current_score=score)
                matches.append(match_model)
            except:
                pass

        print(f"number of scraped matches: {len(matches)}")
        return matches

    def _build_driver(self, url: str) -> WebDriver:
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options)
        driver.get(url)
        return driver

    def _validate_option_availability(self, dropdown_options: List[str]):
        if self.dropdown_option not in dropdown_options:
            raise ValueError  # todo  NoSuchDropdownOptionError

    def _select_dropdown_option(self, dropdown: Select):
        dropdown.select_by_value("Match Odds")

    def _get_matches_list(self, driver):
        matches = driver.find_element_by_id('matchs')
        match_list_elems = matches.find_elements_by_xpath('./div')
        return match_list_elems
