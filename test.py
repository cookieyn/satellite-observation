import xlrd

def read_excel():
    # 打开文件
    workbook = xlrd.open_workbook(r'global.xls')
    # 获取所有sheet
    print (workbook.sheet_names()) # [u'sheet1', u'sheet2']
    #获取sheet2
    sheet2_name= workbook.sheet_names()[1]
    print (sheet2_name)
    # 根据sheet索引或者名称获取sheet内容
    sheet2 = workbook.sheet_by_name(sheet2_name)
    # sheet的名称，行数，列数
    print (sheet2.name,sheet2.nrows,sheet2.ncols)
    rows = sheet2.row_values(1) # 获取第四行内容
    cols = sheet2.col_values(0) # 获取第三列内容
    print (rows)
    print (cols)
    print (sheet2.cell(1,0).value)
     # 获取单元格内容的数据类型
    #print (sheet2.cell(1,0).ctype)
if __name__ == '__main__':
    read_excel()
