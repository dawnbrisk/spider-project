import pdfplumber
import pymysql
import os
import traceback

import re

# ========= 配置 =========
pdf_dir = r"C:\code\picking-list"

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "warehouse_nw",
    "database": "warehouse",
    "charset": "utf8mb4"
}

# ========= 状态 =========
success_count = 0
fail_count = 0
total_files = 0

# ========= 插入函数 =========
def insert_record(cursor, no, locations, sku, qty, size, weight, file_name, page_info):
    global success_count, fail_count
    location_str = " / ".join(locations)
    print(f"📋 解析数据 | No: {no}, SKU: {sku}, QTY: {qty}, Location: {location_str}, Size: {size}, Weight: {weight}, File: {file_name}, Page: {page_info}")
    try:
        cursor.execute(
            """
            INSERT INTO picking_label (no, location, sku, qty, size, weight, file_name, page_info)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (no, location_str, sku, int(qty), size, float(weight) if weight else None, file_name, page_info)
        )
        print("✅ 插入成功\n")
        success_count += 1
    except Exception as e:
        print(f"❌ 插入失败 | 错误: {e}")
        traceback.print_exc()
        fail_count += 1

# ========= 工具函数 =========
def is_sku_qty_line(line):
    parts = line.split()
    return len(parts) == 2 and any(c.isalpha() for c in parts[0]) and parts[1].isdigit()

def is_location_line(line):
    return line.startswith("101") and len(line) > 10

def is_no_line(line):
    return re.fullmatch(r"\d{1,3}", line.strip())

def is_size_line(line):
    return "*" in line and all(c.isdigit() or c in '.*xX ' for c in line)

def is_weight_line(line):
    try:
        float(line.strip())
        return True
    except:
        return False

# ========= 主逻辑 =========
try:
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
except Exception as e:
    print("❌ 无法连接数据库！")
    print(str(e))
    exit(1)

for file_name in os.listdir(pdf_dir):
    if not file_name.lower().endswith(".pdf"):
        continue

    total_files += 1
    full_path = os.path.join(pdf_dir, file_name)
    print(f"\n📄 正在处理文件: {file_name}")

    try:
        with pdfplumber.open(full_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if not text:
                    print("⚠️ 页面无文本，跳过")
                    continue

                lines = text.split("\n")

                # 合并尺寸被拆断的行
                merged_lines = []
                i = 0
                while i < len(lines):
                    line = lines[i].strip()
                    if '*' in line and i + 1 < len(lines):
                        next_line = lines[i + 1].strip()
                        if next_line.replace('.', '').isdigit():
                            merged_lines.append(line + next_line)
                            i += 2
                            continue
                    merged_lines.append(line)
                    i += 1

                page_info = merged_lines[-1] if '/' in merged_lines[-1] else None

                for idx, line in enumerate(merged_lines):
                    line = line.strip()

                    #  如果是 SKU 行
                    if is_sku_qty_line(line):
                        print(f"🔍 识别为 SKU+QTY 行: {repr(line)}")  # ✅ 打印原始行内容
                        parts = line.split()
                        sku = parts[0]
                        qty = parts[1]

                        # 向上查找 No 和 Location
                        locations = []
                        no = None
                        for rev in range(idx - 1, max(idx - 6, -1), -1):
                            up_line = merged_lines[rev].strip()
                            if is_location_line(up_line):
                                locations.insert(0, up_line)
                            elif is_no_line(up_line):
                                no = up_line.strip()
                                break

                        # 向下找 size, weight
                        size = merged_lines[idx + 1].strip() if idx + 1 < len(merged_lines) and is_size_line(merged_lines[idx + 1]) else None
                        weight = merged_lines[idx + 2].strip() if idx + 2 < len(merged_lines) and is_weight_line(merged_lines[idx + 2]) else None

                        print(
                            f"📋 解析数据 | No: {no}, SKU: {sku}, QTY: {qty}, Location:, Size: {size}, Weight: {weight}, File: {file_name}, Page: {page_info}")
                        if no and sku:
                            insert_record(cursor, no, locations, sku, qty, size, weight, file_name, page_info)

    except Exception as err:
        print(f"❌ 处理文件失败: {file_name}")
        traceback.print_exc()

# ========= 结束 =========
conn.commit()
cursor.close()
conn.close()

print("\n📦 所有 PDF 文件处理完毕")
print(f"📁 文件数: {total_files}")
print(f"✅ 成功: {success_count}")
print(f"❌ 失败: {fail_count}")
