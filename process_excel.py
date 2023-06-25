from spliting import split
import torch
from transformers import pipeline

import xlrd
import xlwt

import json

# Инициализируем модельку

device = torch.cuda.current_device() if torch.cuda.is_available() and torch.cuda.mem_get_info()[0] >= 2*1024**3 else -1
model = pipeline("text-classification", "extractor_model", device=device)

# Метод обработки текста моделькой

def process(text: str) -> dict[str, str]:
    result = {"responsibilities": "",
              "requirements": "",
              "terms": "",
              "notes": ""}
    text = text.replace("\t", " ").replace("\r", "")
    sentences = split(text)
    predicts = [predict["label"] for predict in model.predict(sentences)]
    for sentence, label in zip(sentences, predicts):
        result[label.lower()] += sentence + " "
    for key in result.keys():
        result[key] = result[key].strip().replace("  ", " ")
    return result

# Открываем лист excel

COL_IDX = 3
wb = xlrd.open_workbook('preprocessing/data/Датасет.xls', 'rw', formatting_info=True)
wb_sheet = wb.sheet_by_index(0)

# Открываем новую книгу в режиме записи

wb_w = xlwt.Workbook()
wb_w_sheet = wb_w.add_sheet('sheet1')

wb_w_sheet.write(0,0,u'text')
wb_w_sheet.write(0,1,u'responsibilities')
wb_w_sheet.write(0,2,u'requirements')
wb_w_sheet.write(0,3,u'terms')
wb_w_sheet.write(0,4,u'notes')

# Обрабатываем по строкам и сохраняем в новый xls

for row_idx in range(1, wb_sheet.nrows):
    text_cell = wb_sheet.cell(row_idx, COL_IDX).value
    text_original = text_cell
    if not text_cell:
        continue
    prediction = process(text_cell)
    wb_w_sheet.write(row_idx, 0, text_original) # original responsibilities
    wb_w_sheet.write(row_idx, 1, prediction['responsibilities']) # responsibilities
    wb_w_sheet.write(row_idx, 2, prediction['requirements']) # responsibilities
    wb_w_sheet.write(row_idx, 3, prediction['terms']) # responsibilities
    wb_w_sheet.write(row_idx, 4, prediction['notes']) # responsibilities

# Сохраняем новую книгу

wb_w.save('preprocessing/data/Датасет_прогнанный.xls')
