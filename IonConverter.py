import json
import tabula
import os
import sys
from datetime import datetime

text_error = ''
project_name = 'IonConverter'
full_path = os.path.abspath(os.curdir).replace(f'\\{project_name}', '')

# Собираем файлы pdf в массив из каталога FnsTransit
try:

    file_list = []
    for root, dirs, files in os.walk(full_path):
        for file in files:
            if file.endswith(".pdf"):
                file_list.append(os.path.join(root, file))

except Exception:
    e = sys.exc_info()[1]
    text_error = f'error to read files: {e.args[0]}'

# Конвертация файлов из массива
try:

    for current_file in file_list:

        export_data = []
        df_sort_data = []

        # Преобразование файла в датафрейм
        list_of_dfs = tabula.read_pdf(current_file, pages='all', multiple_tables=True)
        # Отсеивание пустых строк
        for i in range(len(list_of_dfs)):
            current_df = list_of_dfs[i]
            df_val = current_df.values
            for current_val in df_val:
                if len(str(current_val[1])) >= 5 and len(str(current_val[2])) >= 5:
                    df_sort_data.append(current_val)

        # Подсчет суммы налогов
        for current_row in df_sort_data:
            tax_sum = 0
            i = 3
            while i < len(current_row):
                current_tax = float(current_row[i].replace(',', '.').replace(' ', ''))
                tax_sum += current_tax
                i += 1
            tax_name = current_row[0] if type(current_row[0]) is str else ''
            json_row = {'name':tax_name.replace('\r', ' '), 'kbk':str(current_row[1]), 'sum':str(tax_sum)}
            export_data.append(json_row)

        # Сохранение файла в json
        with open(current_file.replace('.pdf', '.json'), 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=4)
        
        # Удаление pdf
        os.remove(current_file)
           
except Exception:
    e = sys.exc_info()[1]
    text_error = f'error to convert files: {e.args[0]}'


# Запись ошибки
if text_error != '':
    with open(f'{full_path}\\{project_name}\\error_{datetime.now().strftime("%m_%d_%Y")}.txt', 'w') as file:
        file.write(text_error)
