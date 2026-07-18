import openpyxl
wb = openpyxl.load_workbook("../BUGS IN IQAF HTML.xlsx")
print("Sheets:", wb.sheetnames)
