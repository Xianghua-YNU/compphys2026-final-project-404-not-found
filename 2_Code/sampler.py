"""
sampler.py
--------------------------------------------------------
P3：Bayesian Inference using emcee

读取：
    data/rv_data.csv

调用：
    rv_model.py

输出：
    MCMC samples

AI声明：
本程序在开发过程中参考了 ChatGPT 提供的代码示例，
最终实现及结果均由项目成员完成验证。
"""

import os
import numpy as np
import pandas as pd
import emcee
import matplotlib.pyplot as plt

from rv_model import rv_model

# =====================================================
# 文件路径
# =====================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)

DATA_FILE = os.path.join(
    PROJECT_DIR,
    "3_Data",
    "processed_data",
    "rv_data.csv"
)


RESULT_DIR = os.path.join(BASE_DIR, "results")

os.makedirs(RESULT_DIR, exist_ok=True)

# =====================================================
# 读取数据
# =====================================================

data = pd.read_csv(DATA_FILE)

t = data["JD"].values
rv = data["RV"].values
err = data["Error"].values

print("=" * 50)
print("读取数据成功")
print("=" * 50)

print(f"观测点数 : {len(t)}")
print(f"JD范围 : {t.min():.6f} ~ {t.max():.6f}")

# =====================================================
# 参数说明
#
# theta =
#
# P
# K
# e
# omega
# Tp
# gamma
#
# =====================================================

ndim = 6

# =====================================================
# Prior
# =====================================================

def log_prior(theta):

    P, K, e, omega, Tp, gamma = theta

    if not (1 < P < 10):
        return -np.inf

    if not (0 < K < 100):
        return -np.inf

    if not (0 <= e < 0.9):
        return -np.inf

    if not (0 <= omega < 2*np.pi):
        return -np.inf

    if not (t.min()-20 < Tp < t.max()+20):
        return -np.inf

    if not (-100 < gamma < 100):
        return -np.inf

    return 0.0


# =====================================================
# Gaussian Log Likelihood
# =====================================================

def log_likelihood(theta):

    model = rv_model(theta, t)

    return -0.5 * np.sum(

        ((rv-model)/err)**2

        + np.log(2*np.pi*err**2)

    )


# =====================================================
# Posterior
# =====================================================

def log_probability(theta):

    lp = log_prior(theta)

    if not np.isfinite(lp):

        return -np.inf

    return lp + log_likelihood(theta)


# =====================================================
# 初始参数
#
# 来自文献近似值
# =====================================================

initial = np.array([

    4.2308,     # Period

    56.0,       # Semi amplitude

    0.013,      # eccentricity

    0.7,        # omega

    t.min(),    # Tp

    0.0         # gamma

])

# =====================================================
# 初始化 walker
# =====================================================

nwalkers = 32

pos = initial + 1e-4 * np.random.randn(nwalkers, ndim)

print("\nWalker 初始化完成")
print(f"Walker数量 : {nwalkers}")
print(f"参数维度 : {ndim}")

# =====================================================
# 创建 sampler
# =====================================================

sampler = emcee.EnsembleSampler(

    nwalkers,

    ndim,

    log_probability

)

print("\nemcee 已初始化完成")
print("=" * 50)
# =====================================================
# 开始 MCMC
# =====================================================

print("\n开始 MCMC 采样...\n")

nsteps = 5000

sampler.run_mcmc(
    pos,
    nsteps,
    progress=True
)

print("\n采样完成！")

# =====================================================
# Acceptance Fraction
# =====================================================

acceptance = np.mean(sampler.acceptance_fraction)

print("=" * 50)
print(f"Acceptance Fraction : {acceptance:.3f}")

if acceptance < 0.2:
    print("Walker移动过少，可以增加初始扰动。")

elif acceptance > 0.6:
    print("Walker移动过快，可以调整步长。")

else:
    print("Acceptance Fraction 正常。")

print("=" * 50)

# =====================================================
# Chain
# =====================================================

chain = sampler.get_chain()

print("Chain shape : ", chain.shape)

# =====================================================
# 保存 Chain
# =====================================================

np.save(
    os.path.join(
        RESULT_DIR,
        "chain.npy"
    ),
    chain
)

# =====================================================
# Burn-in
# =====================================================

burnin = 1000

thin = 20

samples = sampler.get_chain(
    discard=burnin,
    thin=thin,
    flat=True
)

print("Posterior Samples :", samples.shape)

# =====================================================
# 保存 Samples
# =====================================================

np.save(
    os.path.join(
        RESULT_DIR,
        "samples.npy"
    ),
    samples
)

# =====================================================
# Autocorrelation Time
# =====================================================

try:

    tau = sampler.get_autocorr_time()

    print("\nAutocorrelation Time")

    for i, value in enumerate(tau):

        print(f"Parameter {i+1} : {value:.2f}")

except Exception:

    print("\n采样步数还不足，无法稳定估计自相关时间。")

# =====================================================
# 输出最佳参数
# =====================================================

labels = [

    "Period",

    "K",

    "e",

    "omega",

    "Tp",

    "gamma"

]

print("\n")

print("=" * 60)

print("Posterior Median")

print("=" * 60)

for i in range(ndim):

    q16, q50, q84 = np.percentile(

        samples[:, i],

        [16, 50, 84]

    )

    plus = q84 - q50

    minus = q50 - q16

    print(

        f"{labels[i]:8s}"

        f" = "

        f"{q50:.6f}"

        f"  +{plus:.6f}"

        f"  -{minus:.6f}"

    )

print("=" * 60)

# =====================================================
# Chain Figure
# =====================================================

fig, axes = plt.subplots(

    ndim,

    figsize=(10, 12),

    sharex=True

)

for i in range(ndim):

    axes[i].plot(

        chain[:, :, i],

        alpha=0.5

    )

    axes[i].set_ylabel(

        labels[i]

    )

axes[-1].set_xlabel(

    "Step"

)

plt.tight_layout()

plt.savefig(

    os.path.join(

        RESULT_DIR,

        "chain.png"

    ),

    dpi=300

)

plt.show()

print("\nChain 图已保存。")

print("Samples 已保存。")

print("\nP3 完成！")