# -*- coding:utf-8 -*-

"""
      ┏┛ ┻━━━━━┛ ┻┓
      ┃　　　　　　 ┃
      ┃　　　━　　　┃
      ┃　┳┛　  ┗┳　┃
      ┃　　　　　　 ┃
      ┃　　　┻　　　┃
      ┃　　　　　　 ┃
      ┗━┓　　　┏━━━┛
        ┃　　　┃   神兽保佑
        ┃　　　┃   代码无BUG！
        ┃　　　┗━━━━━━━━━┓
        ┃　　　　　　　    ┣┓
        ┃　　　　         ┏┛
        ┗━┓ ┓ ┏━━━┳ ┓ ┏━┛
          ┃ ┫ ┫   ┃ ┫ ┫
          ┗━┻━┛   ┗━┻━┛
"""

import openpyxl

letter = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
          'W', 'X', 'Y', 'Z']


def read_excel(filename='data.xlsx', sheet_name='Sheet1', need_line=[], remove_title=False):
    assert max(need_line) < len(letter)
    wb = openpyxl.load_workbook(filename)
    sheet1 = wb[sheet_name]
    col_len = len(sheet1['A'])
    res = []
    for i in range(col_len):
        temp = []

        for each_line in need_line:
            temp_var = letter[each_line] + str(i + 1)
            temp.append(sheet1[temp_var].value)
        res.append(temp)
    if remove_title:
        res = res[1:]
    return res


if __name__ == '__main__':
    print(read_excel('data.xlsx', 'Sheet1', [0, 1], True))
