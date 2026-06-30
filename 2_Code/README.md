# 2_Code/ - 源代码目录

**目的**: 存放所有用于模拟、分析和可视化的代码。代码的质量是评分的重要组成部分。

### **结构原则：**

## 1. prepare_data.py —— 数据预处理

**功能：**

负责读取 NASA Exoplanet Archive 下载的 51 Peg b 原始径向速度数据（TXT 格式），提取有效观测信息，并转换为程序后续分析所需的 CSV 格式。

**主要完成内容：**

- 读取原始 txt 数据；
- 去除注释及无关信息；
- 提取观测时间（JD）；
- 提取径向速度（RV）；
- 提取观测误差（Error）；
- 保存为 `rv_data.csv`。

**输入：**

```
data/
    rv_data.txt
```

**输出：**

```
data/
    rv_data.csv
```

---

## 2. plot_data.py —— 原始数据可视化

**功能：**

读取处理后的 CSV 数据，对原始观测数据进行统计分析，并绘制径向速度观测图。

**主要完成内容：**

- 读取观测数据；
- 输出观测点数量、时间范围及误差统计；
- 绘制带误差棒的径向速度观测图；
- 保存观测图。

**输入：**

```
data/
    rv_data.csv
```

**输出：**

```
rv_observation.png
```

---

## 3. rv_model.py —— 开普勒径向速度模型

**功能：**

实现系外行星的开普勒轨道径向速度模型，是整个项目的核心物理模型。

**主要完成内容：**

- 求解开普勒方程；
- 计算偏近点角（Eccentric Anomaly）；
- 计算真近点角（True Anomaly）；
- 根据轨道参数计算理论径向速度曲线。

**主要参数：**

- P：轨道周期（day）
- K：速度半振幅（m/s）
- e：轨道偏心率
- ω：近点幅角
- Tp：近点通过时刻
- γ：系统速度

**输出：**

理论径向速度序列（Model RV）。

---

## 4. test_model.py —— 模型验证

**功能：**

利用文献给出的 51 Peg b 初始轨道参数，调用 `rv_model.py` 建立理论模型，并与观测数据进行初步比较。

**主要完成内容：**

- 读取观测数据；
- 调用径向速度模型；
- 绘制理论模型曲线；
- 与观测数据进行对比；
- 检查模型是否能够正确运行。

**输出：**

```
rv_compare.png
```

---

## 5. sampler.py —— 贝叶斯参数采样

**功能：**

利用 emcee 实现马尔可夫链蒙特卡罗（MCMC）采样，对轨道参数进行贝叶斯推断。

**主要完成内容：**

- 定义参数先验分布（Prior）；
- 构建高斯似然函数（Likelihood）；
- 构建后验概率函数（Posterior）；
- 初始化 Walker；
- 调用 emcee 进行采样；
- 保存采样结果；
- 输出 Acceptance Fraction；
- 绘制 MCMC Chain 图。

**输入：**

```
data/
    rv_data.csv
```

**输出：**

```
results/

chain.npy

samples.npy

mcmc_chain.png
```

---

## 6. analyse.py —— 后验分析

**功能：**

读取 MCMC 采样结果，对轨道参数进行统计分析，并生成论文所需的图表。

**主要完成内容：**

- 读取 posterior samples；
- 计算参数中位数及 68% 置信区间；
- 绘制 Corner 图；
- 绘制最佳拟合曲线；
- 绘制拟合残差图；
- 输出参数统计表。

**输入：**

```
results/
    samples.npy
```

**输出：**

```
results/

corner_plot.png

best_fit.png

residuals.png

parameter_table.csv
```

---
运行结束后，程序将在 `results` 文件夹中生成所有用于论文和课程汇报的图表及参数统计结果。
### **必需文件：**
- **`README.md` (本文件)**: 必须清晰说明：
    - 每个代码文件的功能。
    - 如何配置环境 (`pip install -r requirements.txt`)。
    - **如何运行主程序**以得到论文中的结果。
      ## 主程序运行方法

完成环境配置后，在 `2_Code` 目录下打开终端，执行以下命令：

```bash
python main.py
```

程序将按照实验流程依次完成以下步骤：

1. 读取并预处理 NASA Exoplanet Archive 提供的原始径向速度数据；
2. 绘制原始径向速度观测图；
3. 建立开普勒径向速度模型；
4. 利用 `emcee` 进行 MCMC 贝叶斯采样；
5. 对采样结果进行后验分析；
6. 生成论文所需的图表及参数统计结果。

程序运行完成后，将自动生成以下主要结果：

```
results/

rv_observation.png      # 原始观测数据图

rv_compare.png          # 理论模型与观测数据对比图

mcmc_chain.png          # MCMC采样链

corner_plot.png         # 后验概率分布图

best_fit.png            # 最佳拟合曲线

residuals.png           # 拟合残差图

parameter_table.csv     # 参数统计结果

samples.npy             # 后验样本

chain.npy               # MCMC采样链数据
```
- **`requirements.txt`**: 项目依赖清单。

### **代码规范要求：**
- **物理注释**: 必须对核心物理方程和算法步骤进行注释。
- **参数化设计**: 物理参数应集中定义，严禁在循环中出现“魔法数字”。
- **AI 声明**: 若使用 AI 辅助编写，需在代码中注明。
