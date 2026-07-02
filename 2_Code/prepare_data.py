"""
prepare_data.py
----------------------------------------
读取 NASA Exoplanet Archive 的原始 RV 数据，
自动生成后续项目使用的 rv_data.csv

输入：
    data/rv_data.txt

输出：
    data/rv_data.csv

AI声明：
本程序在开发过程中参考了 ChatGPT 提供的代码示例，
最终实现及结果均由项目成员完成验证。
"""

import os
import pandas as pd

# prepare_data.py 所在目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 数据文件路径
PROJECT_DIR = os.path.dirname(BASE_DIR)

INPUT_FILE = os.path.join(
    PROJECT_DIR,
    "3_Data",
    "raw_data",
    "rv_data.txt"
)

OUTPUT_FILE = os.path.join(
    PROJECT_DIR,
    "3_Data",
    "processed_data",
    "rv_data.csv"
)

print("脚本目录：", BASE_DIR)
print("输入文件：", INPUT_FILE)
print("文件是否存在：", os.path.exists(INPUT_FILE))

rows = []

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    for line in f:

        line = line.strip()

        # 空行跳过
        if not line:
            continue

        # Header 信息跳过
        if line.startswith("\\"):
            continue

        # 表头跳过
        if line.startswith("JD"):
            continue

        # 数据类型说明跳过
        if line.startswith("double"):
            continue

        # 单位说明跳过
        if line.startswith("days"):
            continue

        # 真正的数据都是以 245 开头
        if line.startswith("245"):

            parts = line.split()

            if len(parts) >= 3:
                rows.append([
                    float(parts[0]),   # JD
                    float(parts[1]),   # RV
                    float(parts[2])    # Error
                ])

# 转成 DataFrame
data = pd.DataFrame(
    rows,
    columns=["JD", "RV", "Error"]
)

# 保存
os.makedirs("data", exist_ok=True)
data.to_csv(OUTPUT_FILE, index=False)

# 输出信息
print("=" * 50)
print("NASA RV 数据读取成功")
print("=" * 50)

print(f"数据点数量 : {len(data)}")
print(f"JD 范围    : {data['JD'].min():.6f} ~ {data['JD'].max():.6f}")
print(f"RV 范围    : {data['RV'].min():.1f} ~ {data['RV'].max():.1f} m/s")
print(f"平均误差   : {data['Error'].mean():.2f} m/s")

print("\n前五行数据：")
print(data.head())

print("\nCSV 已保存：")
print(OUTPUT_FILE)

# 检查数据点数
if len(data) == 256:
    print("\n✓ 成功读取 256 个观测点！")
else:
    print(f"\n⚠ 注意：当前读取到 {len(data)} 个观测点，请检查原始数据文件。")