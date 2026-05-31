import openpyxl

xlsx_path = r"C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\05_PARITY\MTC_V2_PARITY_CASE_TRACKER.xlsx"

wb = openpyxl.load_workbook(xlsx_path)
ws = wb.active

# Rows to add:
new_rows = [
    ["AUTO_047", "L18 - Confirm (Req Raw)", "PENDING_RUN"],
    ["AUTO_048", "L18 - Confirm (Refresh)", "PENDING_RUN"],
    ["AUTO_049", "L21 - Level Retest", "PENDING_RUN"],
]

for row in new_rows:
    ws.append(row)

wb.save(xlsx_path)
print("XLSX updated successfully.")
