import openpyxl

wb = openpyxl.load_workbook("BUGS IN IQAF HTML.xlsx")
sheet = wb.active

for row_idx in range(19, 23):
    row_cells = [sheet.cell(row=row_idx, column=col_idx) for col_idx in range(1, 6)]
    info = []
    for c in row_cells:
        val = c.value
        link = ""
        if c.hyperlink:
            link = f" ({c.hyperlink.target})"
        info.append(f"{val}{link}")
    print(f"Row {row_idx}: {info}")
