"""
test_model.py
--------------------------------------------------------
P2：测试 Keplerian RV Model

功能：
1. 读取 NASA 51 Peg b RV 数据
2. 调用 rv_model.py
3. 绘制观测数据与理论模型
AI声明：
本程序在开发过程中参考了 ChatGPT 提供的代码示例，
最终实现及结果均由项目成员完成验证。
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from rv_model import rv_model

# =====================================================
# 文件路径
# =====================================================



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)

CSV_FILE = os.path.join(
    PROJECT_DIR,
    "3_Data",
    "processed_data",
    "rv_data.csv"
)

# =====================================================
# 读取数据
# =====================================================

data = pd.read_csv(CSV_FILE)

t = data["JD"].values
rv = data["RV"].values
err = data["Error"].values

print("=" * 50)
print("51 Peg b RV 数据")
print("=" * 50)

print(f"观测点数：{len(data)}")
print(f"JD范围：{t.min():.6f} ~ {t.max():.6f}")

# =====================================================
# 文献初始参数（近似）
# =====================================================

theta = [

    4.2308,         # P (day)

    56.0,           # K (m/s)

    0.013,          # e

    0.70,           # omega (rad)

    t.min(),        # Tp

    0.0             # gamma

]

# =====================================================
# 理论模型
# =====================================================

rv_fit = rv_model(theta, t)

# 为了画平滑曲线

t_model = np.linspace(t.min(), t.max(), 2000)

rv_model_curve = rv_model(theta, t_model)

# =====================================================
# 绘图
# =====================================================

plt.figure(figsize=(11,6))

# 观测数据

plt.errorbar(
    t,
    rv,
    yerr=err,
    fmt='o',
    markersize=4,
    capsize=2,
    label="Observed RV"
)

# 理论曲线

plt.plot(
    t_model,
    rv_model_curve,
    linewidth=2,
    label="Initial Kepler Model"
)

plt.xlabel("Julian Date (JD)", fontsize=12)

plt.ylabel("Radial Velocity (m/s)", fontsize=12)

plt.title("51 Peg b Radial Velocity", fontsize=14)

plt.legend()

plt.grid(True)

plt.tight_layout()

# 保存图片

plt.savefig(
    os.path.join(BASE_DIR, "rv_compare.png"),
    dpi=300
)

plt.show()

print("\n图片已保存：rv_compare.png")