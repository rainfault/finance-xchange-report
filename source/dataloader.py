import requests
import json

class Loader:
    def __init__(self, timeout_sec=1) -> None:
        self.timeout_sec = timeout_sec

    def load_json(self, url: str) -> dict:
        """Загрузка данных через GET запрос с сервера."""
        try:
            response = requests.get(url, timeout = self.timeout_sec)
            data = response.json()

        
            filename = 'data.json'

            # with open(filename, 'w') as file:
            #     json.dump(data, file, indent=4)

            return data


        except requests.exceptions.Timeout as e:
            print("Timeout while connection to moex.")