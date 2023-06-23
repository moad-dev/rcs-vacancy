
import xlrd
import xlwt
from xlutils.copy import copy

import json

import re
import sys
def remove_emoji(string):
    emoji_pattern = re.compile("["
    u"\U0001F600-\U0001F64F"  # emoticons
    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
    u"\U0001F680-\U0001F6FF"  # transport & map symbols
    u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
    u"\U00002702-\U000027B0"
    u"\U000024C2-\U0001F251"
    "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)

COL_IDX = 3

wb = xlrd.open_workbook('Датасет.xls', 'rw', formatting_info=True)
wb_sheet = wb.sheet_by_index(0)
wb_w = copy(wb)
wb_w_sheet = wb_w.get_sheet(0)
# wb_w_sheet.write(row_idx, COL_IDX, removed_emojis_value)
# wb_w.save('Датасет.xls')
values = []

for row_idx in range(1, wb_sheet.nrows):
    text_cell = wb_sheet.cell(row_idx, COL_IDX).value
    text_cell_xf = wb.xf_list[wb_sheet.cell_xf_index(row_idx, COL_IDX)]
    if not text_cell:
        continue
    text_cell_runlist = wb_sheet.rich_text_runlist_map.get((row_idx, COL_IDX))
    if text_cell_runlist:
        deleted = 0
        for segment_idx in range(len(text_cell_runlist)):
            font = wb.font_list[text_cell_runlist[segment_idx][1]]
            color = wb.colour_map.get( font.colour_index  )
            if (color is not None):
                if (color[0] == 0 and color[1] == 176 and color[2] == 80):
                    offset = text_cell_runlist[segment_idx][0]
                    if segment_idx == len(text_cell_runlist)-1 :
                        text_cell = text_cell[:offset-deleted]
                    else:
                        next_offset = text_cell_runlist[segment_idx+1][0]
                        text_cell = text_cell[:offset-deleted] + text_cell[next_offset-deleted:]
                        deleted += next_offset-offset
    print("\n\n"+text_cell+"\n\n")
