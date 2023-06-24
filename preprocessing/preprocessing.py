
import xlrd
import xlwt

import json

def get_front_color(xf, wb):
    font = wb.font_list[xf.font_index]
    if not font:
        return None
    return get_color(font.colour_index, wb)
def get_back_color(xf, wb):
    if not xf.background:
        return None
    return get_color(xf.background.background_colour_index, wb)
def get_color(color_index, wb):
    return wb.colour_map.get(color_index)
def get_if_protected(xf):
    if not xf.protection:
        return False
    return xf.protection.cell_locked

COL_IDX = 3

wb = xlrd.open_workbook('data/Датасет.xls', 'rw', formatting_info=True)
wb_sheet = wb.sheet_by_index(0)

wb_w = xlwt.Workbook()
wb_w_sheet = wb_w.add_sheet('sheet1')

wb_w_sheet.write(0,0,u'text')
wb_w_sheet.write(0,1,u'responsibilities')
wb_w_sheet.write(0,2,u'modified')
wb_w_sheet.write(0,3,u'requirements')
wb_w_sheet.write(0,4,u'terns')
wb_w_sheet.write(0,5,u'notes')

for row_idx in range(1, wb_sheet.nrows):
    text_cell = wb_sheet.cell(row_idx, COL_IDX).value
    original_responsibilities = text_cell
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
    else:
        c = wb_sheet.cell(row_idx, COL_IDX)
        xf = wb.xf_list[c.xf_index]
        color = get_front_color(xf, wb)
        if (color is not None):
            if (color[0] == 0 and color[1] == 176 and color[2] == 80):
                text_cell = u''

    wb_w_sheet.write(row_idx, 0, original_responsibilities) # original responsibilities
    wb_w_sheet.write(row_idx, 1, text_cell) # cleaned responsibilities
    wb_w_sheet.write(row_idx, 2, 0 if text_cell == original_responsibilities else 1) # is green text has been found
    wb_w_sheet.write(row_idx, 3, wb_sheet.cell(row_idx, 4).value) # requirements
    wb_w_sheet.write(row_idx, 4, wb_sheet.cell(row_idx, 5).value) # terns
    notes = wb_sheet.cell(row_idx, 16).value
    wb_w_sheet.write(row_idx, 5, u"" if notes == u"\\N" else notes) # notes

wb_w.save('data/Датасет_обработанный.xls')
