# 경비 정리표 만들기 — receipts.json → 엑셀(경비 내역 + 분류별 합계 원그래프). 개인카드·현금은 노란색 + '따로 청구'
# 사용: python3 make_expense.py receipts.json 9월_경비정리.xlsx
import json, sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import PieChart, Reference
R = json.load(open(sys.argv[1], encoding='utf8')); out = sys.argv[2]
wb = Workbook(); ws = wb.active; ws.title = '경비 내역'
ws.append(['날짜', '사용처', '분류', '내용', '금액(원)', '결제', '비고'])
for r in R:
    note = r.get('note', '')
    if r['pay'] in ('개인카드', '현금') and '따로' not in note: note = (note + ' ' if note else '') + f"{r['pay']} → 따로 청구"
    ws.append([r['date'], r['store'], r['category'], r['items'], r['amount'], r['pay'], note])
n = len(R) + 1; ws.append(['', '', '', '합계', f'=SUM(E2:E{n})', '', ''])
thin = Side(style='thin', color='CCCCCC')
for c in ws[1]: c.font = Font(bold=True, color='FFFFFF'); c.fill = PatternFill('solid', fgColor='1F2A44'); c.alignment = Alignment(horizontal='center')
for row in ws.iter_rows(min_row=2, max_row=n + 1):
    for c in row: c.border = Border(top=thin, bottom=thin, left=thin, right=thin)
    row[4].number_format = '#,##0'
    if row[6].value and ('따로' in str(row[6].value) or '확인 필요' in str(row[6].value)):
        for c in row: c.fill = PatternFill('solid', fgColor='FFF4CC')
for col, w in zip('ABCDEFG', [12, 18, 10, 30, 12, 16, 22]): ws.column_dimensions[col].width = w
s = wb.create_sheet('분류별 합계'); s.append(['분류', '금액(원)']); cats = {}
for r in R: cats[r['category']] = cats.get(r['category'], 0) + r['amount']
for k, v in cats.items(): s.append([k, v])
pie = PieChart(); pie.title = '분류별 경비'
pie.add_data(Reference(s, min_col=2, min_row=1, max_row=len(cats) + 1), titles_from_data=True); pie.set_categories(Reference(s, min_col=1, min_row=2, max_row=len(cats) + 1)); s.add_chart(pie, 'D2')
wb.save(out); print(f'{len(R)}건 · 합계 {sum(r["amount"] for r in R):,}원 · 따로 청구 {sum(1 for r in R if r["pay"] in ("개인카드", "현금"))}건 → {out}')
