import pandas as pd
import win32com.client as win32
from openpyxl import load_workbook
from config import EXCEL_FILEPATH
from config import EXCEL_FILEPATH

class DataProcessor:
    
    DATAFRAMES = []

    def __init__(self) -> None:
        pass
 
    def json_to_dataframe(self, data: dict):
        """Преобразует полученные данные после GET-запроса в Dataframe."""
        df = pd.DataFrame(data["securities"]["data"], columns=data["securities"]["columns"])

        df_vk = df[df["clearing"] == "vk"]

        df_filtered = df_vk[["tradedate", "rate", "tradetime"]]
        df_filtered.reset_index(drop=True, inplace=True)

        self.DATAFRAMES.append(df_filtered)
        
        return df_filtered
    

    def dataframe_to_excel(self) -> int:
        """Объединение таблицы, добавление столбца G и запись в excel-файл."""
        
        # Мерж котировок и добавление столбца их отношений
        df1, df2 = self.DATAFRAMES[0], self.DATAFRAMES[1]

        merged_df = pd.concat((df1, df2), axis=1)
        
        merged_df['ratio'] = (df1['rate'] / df2['rate']).round(2)
  
        new_column_names = ['Дата USD/RUB', 'Курс USD/RUB', 'Время USD/RUB', 
                            'Дата JPY/RUB', 'Курс JPY/RUB', 'Время JPY/RUB', 
                            'Результат']
        
        # merged_df['Курс USD/RUB'] = merged_df['Курс USD/RUB'].round(2)
        # merged_df['Курс JPY/RUB'] = merged_df['Курс USD/RUB'].round(2)
        # merged_df['Результат'] = merged_df['Курс USD/RUB'].round(2)
        
        merged_df.columns = new_column_names

        # Запись в excel файл / настройка файла 
        with pd.ExcelWriter(EXCEL_FILEPATH, engine='xlsxwriter') as writer:
            merged_df.to_excel(writer, index=False, sheet_name='Rates')

            # Получаем объект workbook и активный лист
            workbook = writer.book
            worksheet = writer.sheets['Rates']

            financial_format = workbook.add_format({'num_format': '#,##0.00;(#,##0.00)', 'align': 'right'})
            center_format = workbook.add_format({'align': 'center'})

            # Автовыравнивание и применение требуемых форматов
            for column, label in enumerate(merged_df.columns):
                series = merged_df[label]
  
                max_len = max((
                    series.astype(str).map(len).max(), 
                    len(str(series.name))  
                )) + 1
                current_format = financial_format if label in ("Курс USD/RUB", "Курс JPY/RUB", "Результат") else center_format                 
                worksheet.set_column(column, column, max_len, current_format) 

        return merged_df.shape[0]
    
    def verify_autosum(self):
        """Проверка корректности работы автосуммы."""

        workbook = load_workbook(filename=EXCEL_FILEPATH)
        sheet = workbook.active 
        sheet['G22'] = '=SUM(G2:G21)'
        workbook.save(filename=EXCEL_FILEPATH)

        excel = win32.gencache.EnsureDispatch('Excel.Application')

        try:
            workbook = excel.Workbooks.Open(EXCEL_FILEPATH)
            sheet = workbook.ActiveSheet
            excel.Calculate()
            
            sum_value = sheet.Range('G22').Value

            assert type(sum_value) in (int, float), "Сумма должна быть целым числом!" 

            sheet.Range('G22').ClearContents()

            workbook.Save()
            workbook.Close()

        except Exception as e:
            print(f'Ошибка: {e}')
        finally:
            excel.Quit()

    

    