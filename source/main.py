import unittest
from dataloader import Loader
from dataprocessor import DataProcessor
from sender import Sender
from tabletests import TestExcelFile

from config import USD_TO_RUB_URL, JPY_TO_RUB_URL


if __name__ == "__main__":
    
    loader = Loader()
    
    # Загрузка котировок доллара к рублю USD/RUB
    dollar_to_rub_data = loader.load_json(USD_TO_RUB_URL)
    print("USD/RUB Курс сформирован.")

    # Загрузка котировок японской йены к рублю JPY/RUB
    yen_to_rub_data = loader.load_json(JPY_TO_RUB_URL)
    print("JPY/RUB Курс сформирован.")

    print("Обработка..")
    processor = DataProcessor()
    processor.json_to_dataframe(dollar_to_rub_data)
    processor.json_to_dataframe(yen_to_rub_data)
    total_rows = processor.dataframe_to_excel()
    processor.verify_autosum()
    print("Обработка данных завершена. Тестирую итоговую таблицу...")

    # Запуск тестов
    suite = unittest.TestLoader().loadTestsFromTestCase(TestExcelFile)
    result = unittest.TextTestRunner().run(suite)

    if result.wasSuccessful():
        print("Отправляю письмо на почту...")
        sender = Sender()
        sender.send_with_attachment(total_rows)
    else:
        print("Письмо не было отправлено из-за некорректных данных в таблице.")
    