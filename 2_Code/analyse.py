"""
analyse.py
--------------------------------------------------------
P4:MCMC 后验分析

功能：

1. 读取 samples.npy
2. 计算最佳参数
3. Corner Plot
4. Best Fit
5. Residual
6. 输出参数统计

AI声明:
本程序在开发过程中参考了 ChatGPT 提供的代码示例，
最终实现及结果均由项目成员完成验证。
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import corner

from rv_model import rv_model

# =====================================================
# 路径
# =====================================================



RESULT_DIR = os.path.join(BASE_DIR, "results")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)

DATA_FILE = os.path.join(
    PROJECT_DIR,
    "3_Data",
    "processed_data",
    "rv_data.csv"
)

samples = np.load(os.path.join(RESULT_DIR, "samples.npy"))

data = pd.read_csv(DATA_FILE)

t = data["JD"].values
rv = data["RV"].values
err = data["Error"].values

labels = [

    "P (day)",

    "K (m/s)",

    "e",

    "ω",

    "Tp",

    "γ"

]

print("="*60)
print("Posterior Analysis")
print("="*60)

# =====================================================
# 中位数参数
# =====================================================

theta_best = np.median(samples, axis=0)

print("\nBest Parameters\n")

table = []

for i in range(len(labels)):

    q16, q50, q84 = np.percentile(

        samples[:, i],

        [16, 50, 84]

    )

    plus = q84 - q50

    minus = q50 - q16

    print(

        f"{labels[i]:10s}"

        f"{q50:.6f}"

        f" +{plus:.6f}"

        f" -{minus:.6f}"

    )

    table.append(

        [labels[i], q50, plus, minus]

    )

# =====================================================
# 保存参数表
# =====================================================

parameter_table = pd.DataFrame(

    table,

    columns=[

        "Parameter",

        "Median",

        "+1sigma",

        "-1sigma"

    ]

)

parameter_table.to_csv(

    os.path.join(

        RESULT_DIR,

        "parameter_table.csv"

    ),

    index=False

)

print("\n参数表已保存。")

# =====================================================
# Corner Plot
# =====================================================

fig = corner.corner(

    samples,

    labels=labels,

    show_titles=True,

    title_fmt=".4f",

    quantiles=[0.16,0.5,0.84]

)

fig.savefig(

    os.path.join(

        RESULT_DIR,

        "corner_plot.png"

    ),

    dpi=300

)

plt.close(fig)

print("Corner Plot 已保存。")

# =====================================================
# Best Fit
# =====================================================

rv_best = rv_model(

    theta_best,

    t

)

t_model = np.linspace(

    t.min(),

    t.max(),

    3000

)

rv_curve = rv_model(

    theta_best,

    t_model

)

plt.figure(figsize=(10,6))

plt.errorbar(

    t,

    rv,

    yerr=err,

    fmt='o',

    ms=4,

    capsize=2,

    label="Observation"

)

plt.plot(

    t_model,

    rv_curve,

    lw=2,

    label="Best Fit"

)

plt.xlabel("Julian Date")

plt.ylabel("Radial Velocity (m/s)")

plt.title("Best-fit Keplerian RV")

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.savefig(

    os.path.join(

        RESULT_DIR,

        "best_fit.png"

    ),

    dpi=300

)

plt.show()

# =====================================================
# Residual
# =====================================================

residual = rv - rv_best

plt.figure(figsize=(10,4))

plt.errorbar(

    t,

    residual,

    yerr=err,

    fmt='o',

    ms=4,

    capsize=2

)

plt.axhline(

    0,

    color='red',

    linestyle='--'

)

plt.xlabel("Julian Date")

plt.ylabel("Residual (m/s)")

plt.title("Residual")

plt.grid(True)

plt.tight_layout()

plt.savefig(

    os.path.join(

        RESULT_DIR,

        "residuals.png"

    ),

    dpi=300

)

plt.show()

print("Residual 图已保存。")

print("\n全部分析完成！")