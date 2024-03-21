from dataloader import Loader
from dataprocessor import DataProcessor
from sender import Sender
from config import *


if __name__ == "__main__":
    
    loader = Loader()
    
    # Загрузка котировок доллара к рублю USD/RUB
    dollar_to_rub_data = loader.load_json(USD_TO_RUB_URL)
    print("USD/RUB Loading done.")

    # Загрузка котировок японской йены к рублю JPY/RUB
    yen_to_rub_data = loader.load_json(JPY_TO_RUB_URL)
    print("JPY/RUB Loading done.")


    processor = DataProcessor()

    processor.json_to_dataframe(dollar_to_rub_data)
    processor.json_to_dataframe(yen_to_rub_data)
    processor.dataframe_to_excel()



