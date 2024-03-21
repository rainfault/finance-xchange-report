import pandas as pd
import openpyxl

class DataProcessor:
    
    DATAFRAMES = []
    EXCEL_FILEPATH = "output/statistics.xlsx"

    def __init__(self) -> None:
        pass
 
    def json_to_dataframe(self, data: dict):
        # Преобразование данных в DataFrame
        df = pd.DataFrame(data["securities"]["data"], columns=data["securities"]["columns"])

        # Фильтрация строк, где 'clearing' равно 'vk'
        df_vk = df[df["clearing"] == "vk"]

        # Выбор нужных столбцов
        df_filtered = df_vk[["tradedate", "rate", "tradetime"]]
        df_filtered.reset_index(drop=True, inplace=True)

        self.DATAFRAMES.append(df_filtered)

        # print("Frame done!")
        # print("==============")
        # print(df_filtered)
        # print("==============")

        return df_filtered
    

    def dataframe_to_excel(self):
        """Объединение таблицы, добавление столбца G и запись в excel-файл."""
        # Мерж котировок и добавление столбца их отношений
        
        df1, df2 = self.DATAFRAMES[0], self.DATAFRAMES[1]

        merged_df = pd.concat((df1, df2), axis=1)
        
        merged_df['ratio'] = df1['rate'] / df2['rate']

        new_column_names = ['Дата USD/RUB', 'Курс USD/RUB', 'Время USD/RUB', 
                            'Дата JPY/RUB', 'Курс JPY/RUB', 'Время JPY/RUB', 
                            'Результат']

        merged_df.columns = new_column_names

        # Запись в excel файл / настройка файла 
        with pd.ExcelWriter(self.EXCEL_FILEPATH, engine='openpyxl') as writer:
            merged_df.to_excel(writer, index=False, sheet_name='Rates')

            # Получаем объект workbook и активный лист
            workbook = writer.book
            worksheet = writer.sheets['Rates']

            # Делаю автоматическое выравнивание по ширине
            













