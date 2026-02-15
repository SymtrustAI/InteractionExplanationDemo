# 🔍 Interaction Explanation  
### 面向大语言模型的 AND–OR 逻辑交互分析框架  

**创业公司 Demo · 模型推理透明化 · 跨模型机理分析**

[English](README.md) | [中文](README_zh.md)

![Python](https://img.shields.io/badge/Python-3.10-blue.svg)  
![CUDA](https://img.shields.io/badge/CUDA-Required-green.svg)  
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)  
![Release](https://img.shields.io/badge/Release-v1.0-black.svg)

---


## 🚀 为什么重要

大语言模型能力强大，但内部推理机制高度不透明。

**Interaction Explanation** 聚焦于揭示 LLM 推理过程中的 AND–OR 逻辑交互结构。

我们不仅关注输出结果，更关注：

- 🧠 Token 之间如何发生交互  
- 🌳 推理过程中形成了哪些结构模式  
- 📊 交互强度如何分布与集中  
- ⚖ 不同模型之间推理逻辑的差异  

本仓库是 SymTrustAI 在 LLM 评估与可解释性方向能力的技术演示。

## 🌐 体验在线 Demo

在我们的在线平台上探索真实的机理交互分析结果：

👉 [立即访问 Demo](https://www.symtrustai.com/demo)


---

## 🧠 我们展示的能力

### AND–OR 交互提取  
提取输入 token 之间结构化的 AND–OR 逻辑交互关系。

### 交互稀疏性分析  
量化交互结构的稀疏性，表明仅需少量关键交互即可忠实解释大语言模型的推理逻辑。

### 逻辑交互树构建  
基于显著交互构建可解释的 AND–OR 逻辑树，能够在掩码输入提示下近似复现模型的输出行为。

### 跨模型机理对比  
系统性比较 DeepSeek 与 Qwen 模型的交互结构，揭示其底层推理机制的差异。


---

## 🧪 支持的模型配置

### 🟢 小规模模式（1.5B）

| 模型 1 | 模型 2 |
|----------|----------|
| deepseek-r1-distill-qwen-1.5b | qwen2.5-1.5b |

运行方式：

    python ./demo --model_size small

适用于显存较小环境或快速实验。

---

### 🔵 大规模模式（7B / 8B）— 默认

| 模型 1 | 模型 2 |
|----------|----------|
| deepseek-r1-distill-llama-8b | qwen2.5-7b |

运行方式：

    python ./demo

适用于完整结构分析。

---

## ⚙ 安装说明

环境要求：

- Python 3.10  
- Conda  
- 支持 CUDA 的 GPU  

安装步骤：

    conda create -n interaction python=3.10
    conda activate interaction
    cd InteractionExplanationDemo
    pip install -r requirements.txt

---

## 🚀 快速开始

默认运行：

    python ./demo

小规模模式：

    python ./demo --model_size small

---

## 🛠 命令行参数

| 参数 | 默认值 | 说明 |
|----------|----------|-------------|
| `--gpu_id` | 1 | GPU 设备编号 |
| `--cal_batch_size` | 128 | 掩码前向计算批大小 |
| `--model_size` | large | small 或 large |

如显存不足，请适当降低 `--cal_batch_size`。

---

## 📝 自定义输入（进阶）

<details>
<summary><b>点击展开配置说明</b></summary>

### 步骤 1 — 删除默认示例

    rm datasets/custom-generation-test/sentences.txt
    rm -rf players/custom-generation-test/players-qwen-manual/*

---

### 步骤 2 — 添加输入句子

保存至：

    datasets/custom-generation-test/sentences.txt

要求：

- 10–20 个单词  
- 不可重复  
- 需具备语义信息  

---

### 步骤 3 — 定义 Player

创建文件：

    players/custom-generation-test/player_words.json

要求：

- 8–15 个 player  
- 顺序必须与原句一致  
- 不可为纯标点  
- 避免语义弱词（如 and, to, the）

</details>

---

## 📊 输出内容

每个模型会生成：

- generation.txt  
- inference.txt  
- interaction.txt  
- sparsity.png  
- interaction_tree.pdf  

跨模型对比结果存储在：

    generalizable_interaction/

---

## 💻 硬件建议

| 模式 | 推荐显存 |
|------|------------------|
| small | ≥ 10GB |
| large | ≥ 32GB |

---

## 💡 创业愿景

我们相信，可解释性是构建可信 AI 系统的基础，包括：

- 更可靠的模型  
- 更安全的部署  
- 更透明的模型评估  
- 更标准化的跨模型对比  

本 Demo 展示了我们的结构化推理分析能力。  
不包含内部生产系统实现。

---

## 📜 许可证

Apache License 2.0
