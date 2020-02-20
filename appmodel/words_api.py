import json
from typing import List
import requests
from config import Config


class WordsApi:

    @staticmethod
    def get_definitions(word: str) -> List[str]:

        url = f'https://wordsapiv1.p.rapidapi.com/words/{word}/definitions'

        headers = {
            'x-rapidapi-host': Config.WORDSAPI_HOST,
            'x-rapidapi-key': Config.WORDSAPI_KEY
            }

        response = requests.request("GET", url, headers=headers)

        result = []
        if not response or response.status_code == '200':
            return result

        for definition in json.loads(response.text)['definitions']:
            result.append(definition['definition'])
        return result


if __name__ == '__main__':
    WordsApi.get_definitions('solution')

