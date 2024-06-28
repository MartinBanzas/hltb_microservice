from typing import List
import requests
from pydantic import BaseModel

class Game(BaseModel):
    game_img: str
    game_name: str
    game_main: str
    game_extra: str
    game_completionist: str
    release_world: int
    profile_dev: str

class HLTB:
    BASE_URL = "https://howlongtobeat.com/"
    SEARCH_URL = BASE_URL + "api/search"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Content-Type': 'application/json',
        'If-None-Match': 'wyzzy',
        'Accept': '*/*',
        'Origin': 'https://howlongtobeat.com',
        'Referer': 'https://howlongtobeat.com'
    }
           
    payload = {
        "searchType": "games",
        "searchTerms": [],
        "searchPage": 1,
        "size": 20,
        "searchOptions": {
            "games": {
                "userId": 0,
                "platform": "",
                "sortCategory": "popular",
                "rangeCategory": "main",
                "rangeTime": {
                    "min": 0,
                    "max": 0
                },
                "gameplay": {
                    "perspective": "",
                    "flow": "",
                    "genre": ""
                },
                "modifier": ""
            },
            "users": {
                "sortCategory": "postcount"
            },
            "filter": "",
            "sort": 0,
            "randomizer": 0
        }
    }

    def search(self, title: str) -> List[Game]:
        self.payload['searchTerms'] = [title]
        try:
            response = requests.post(self.SEARCH_URL, json=self.payload, headers=self.headers)
            response.raise_for_status()
            formatted_response = self.format_json(response.json())
            
            if not formatted_response:
                return {"error": "No results for this query"}
            else:    
                return formatted_response
        except Exception as e:
            print("Error:", e)
            

    def format_json(self, response: dict) -> List[Game]:
        formatted_json = []
        for element in response.get('data', []):
            try:
                game = Game(
                    game_img="https://howlongtobeat.com/games/" + element['game_image'],
                    game_name=element['game_name'],
                    game_main=self.format_time(element['comp_main']),
                    game_extra=self.format_time(element['comp_plus']),
                    game_completionist=self.format_time(element['comp_100']),
                    release_world=element['release_world'],
                    profile_dev=element['profile_dev']
                )
               
                formatted_json.append(game)
            except KeyError as e:
                print(f"Missing key in response: {e}")
        return formatted_json

    @staticmethod
    def format_time(time: int) -> str:
        hours = time // 3600
        minutes = (time % 3600) // 60
        return f"{hours}h {minutes}min"