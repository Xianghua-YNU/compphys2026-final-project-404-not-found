"""
rv_model.py
---------------------------------------------------
P2：建立开普勒径向速度模型（Keplerian RV Model）

模型：

v(t)=γ+K[cos(ω+f)+e cosω]

其中：

P      轨道周期(day)
K      径向速度半振幅(m/s)
e      偏心率
ω      近点幅角(rad)
Tp     近点通过时刻(JD)
γ      系统速度(m/s)

AI声明：
本程序在开发过程中参考了 ChatGPT 提供的代码示例，
最终实现及结果均由项目成员完成验证。
"""

import numpy as np
from scipy.optimize import newton
import matplotlib.pyplot as plt


# =====================================================
# 求解 Kepler 方程
# =====================================================

def eccentric_anomaly(M, e):
    """
    求解 Kepler 方程

    M = E - e sin(E)

    Parameters
    ----------
    M : float
        Mean anomaly

    e : float
        Orbital eccentricity

    Returns
    -------
    E : float
        Eccentric anomaly
    """

    # 保证 M 在 [0,2π]
    M = np.mod(M, 2*np.pi)

    func = lambda E: E - e*np.sin(E) - M

    return newton(func, M)


# =====================================================
# 偏近点角 -> 真近点角
# =====================================================

def true_anomaly(E, e):
    """
    Convert eccentric anomaly to true anomaly
    """

    return 2*np.arctan2(
        np.sqrt(1+e)*np.sin(E/2),
        np.sqrt(1-e)*np.cos(E/2)
    )


# =====================================================
# Keplerian RV Model
# =====================================================

def rv_model(theta, t):
    """
    Keplerian Radial Velocity Model

    Parameters
    ----------
    theta

        theta=[

            P,

            K,

            e,

            omega,

            Tp,

            gamma

        ]

    t

        Observation time

    Returns
    -------

    rv

        Radial velocity
    """

    P, K, e, omega, Tp, gamma = theta

    M = 2*np.pi*(t-Tp)/P

    f = np.zeros(len(t))

    for i in range(len(t)):

        Ei = eccentric_anomaly(M[i], e)

        f[i] = true_anomaly(Ei, e)

    rv = gamma + K*(np.cos(omega+f)+e*np.cos(omega))

    return rv


# =====================================================
# 测试程序
# =====================================================

if __name__ == "__main__":

    # 时间
    t = np.linspace(0, 20, 1000)

    # 51 Peg b 文献参数（近似）
    theta = [

        4.2308,     # Period (day)

        56.0,       # Semi-amplitude (m/s)

        0.013,      # Eccentricity

        0.7,        # omega (rad)

        0.0,        # Tp

        0.0         # gamma

    ]

    rv = rv_model(theta, t)

    plt.figure(figsize=(10,5))

    plt.plot(
        t,
        rv,
        lw=2
    )

    plt.xlabel("Time (day)", fontsize=12)

    plt.ylabel("Radial Velocity (m/s)", fontsize=12)

    plt.title("Keplerian Radial Velocity Model", fontsize=14)

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        "rv_model_test.png",
        dpi=300
    )

    plt.show()