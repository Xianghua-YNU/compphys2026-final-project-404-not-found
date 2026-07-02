"""
AI声明：
本程序在开发过程中参考了 ChatGPT 提供的代码示例，
最终实现及结果均由项目成员完成验证。
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

# 当前脚本所在目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# CSV 文件路径
CSV_FILE = os.path.join(BASE_DIR, "data", "rv_data.csv")

# 读取数据
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)

DATA_FILE = os.path.join(
    PROJECT_DIR,
    "3_Data",
    "processed_data",
    "rv_data.csv"
)

data = pd.read_csv(DATA_FILE)

t = data["JD"]
rv = data["RV"]
err = data["Error"]

print("=" * 50)
print("数据统计")
print("=" * 50)
print(f"观测点数：{len(data)}")
print(f"JD范围：{t.min():.6f} ~ {t.max():.6f}")
print(f"RV范围：{rv.min():.1f} ~ {rv.max():.1f} m/s")
print(f"平均误差：{err.mean():.2f} m/s")

plt.figure(figsize=(10, 6))

plt.errorbar(
    t,
    rv,
    yerr=err,
    fmt='o',
    markersize=4,
    capsize=3
)

plt.xlabel("Julian Date (JD)")
plt.ylabel("Radial Velocity (m/s)")
plt.title("51 Peg Radial Velocity")

plt.grid(True)

plt.tight_layout()

# 图片保存到脚本目录
plt.savefig(os.path.join(BASE_DIR, "rv_observation.png"), dpi=300)

plt.show()