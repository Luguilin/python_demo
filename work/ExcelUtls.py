from openpyxl import Workbook
from openpyxl import load_workbook




# 文档地址
# https://openpyxl.readthedocs.io/en/stable/

# https://openpyxl.readthedocs.io/en/stable/tutorial.html#accessing-many-cells



def get_table(file_path):

    wb = load_workbook(file_path)
    sheet = wb["年后"]
    list_sheet1=sheet['G:H']
    for row in list_sheet1:
        for cloun in row:
            print(cloun.value)

get_table("./1111.xlsx")
