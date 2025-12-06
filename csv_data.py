import re
import csv

def parse_sql_to_csv(sql_file: str, csv_file: str) -> None:
    columns = [
        'IDNTN', 'TuNgu', 'SoTu', 'PhienAm', 'IPA', 'LoaiTu', 
        'PhaiSinh', 'SoNghia', 'NghiaTiengViet', 'GhiChu', 
        'XemNhu', 'MoTa1', 'MoTa2', 'MoTa3', 'MoTa4'
    ]
    
    pattern = re.compile(r"\((\d+),\s*'((?:[^'\\]|\\.|'')*)',\s*(\d+),\s*'((?:[^'\\]|\\.|'')*)',\s*'((?:[^'\\]|\\.|'')*)',\s*'((?:[^'\\]|\\.|'')*)',\s*'((?:[^'\\]|\\.|'')*)',\s*(\d+),\s*'((?:[^'\\]|\\.|'')*)',\s*'((?:[^'\\]|\\.|'')*)',\s*'((?:[^'\\]|\\.|'')*)',\s*'((?:[^'\\]|\\.|'')*)',\s*'((?:[^'\\]|\\.|'')*)',\s*'((?:[^'\\]|\\.|'')*)',\s*'((?:[^'\\]|\\.|'')*)'\)")
    
    rows = []
    with open(sql_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for match in pattern.finditer(content):
        row = [
            int(match.group(1)),
            match.group(2).replace("''", "'"),
            int(match.group(3)),
            match.group(4).replace("''", "'"),
            match.group(5).replace("''", "'"),
            match.group(6).replace("''", "'"),
            match.group(7).replace("''", "'"),
            int(match.group(8)),
            match.group(9).replace("''", "'"),
            match.group(10).replace("''", "'"),
            match.group(11).replace("''", "'"),
            match.group(12).replace("''", "'"),
            match.group(13).replace("''", "'"),
            match.group(14).replace("''", "'"),
            match.group(15).replace("''", "'")
        ]
        rows.append(row)
    
    with open(csv_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        writer.writerows(rows)

if __name__ == '__main__':
    parse_sql_to_csv('taidamtb.sql', 'corpus.csv')
