"""
main.py
--------------------------------------------------------
程序入口

功能：
1. 数据预处理
2. 原始数据可视化
3. MCMC 贝叶斯采样
4. 后验分析

运行方式：
python main.py

AI声明：
本程序在开发过程中参考了 ChatGPT 提供的代码示例，
最终实现及结果均由项目成员完成验证。
"""

import subprocess
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

scripts = [
    "prepare_data.py",
    "plot_data.py",
    "sampler.py",
    "analyse.py"
]

print("=" * 60)
print("51 Peg b 径向速度贝叶斯拟合")
print("=" * 60)

for script in scripts:

    print(f"\n>>> 正在运行：{script}")

    subprocess.run(
        [sys.executable, os.path.join(BASE_DIR, script)],
        check=True
    )

print("\n" + "=" * 60)
print("全部程序运行完成！")
print("结果已保存在 results 文件夹。")
print("=" * 60)