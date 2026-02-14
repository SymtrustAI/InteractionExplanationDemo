<p align="right">
<a href="README.md">English</a> | <a href="README_zh.md">中文</a>
</p>

# InteractionExplanationDemo
### 面向大语言模型的 AND–OR 逻辑交互分析框架

[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)]()
[![CUDA](https://img.shields.io/badge/CUDA-Required-green.svg)]()
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)
[![Release](https://img.shields.io/badge/Release-v1.0-black.svg)]()
[![Status](https://img.shields.io/badge/Status-First%20Public%20Release-brightgreen.svg)]()

---

## 项目简介

**Interaction Explanation** 是一个面向大语言模型（LLMs）的研究型框架，用于提取与分析模型内部的 AND–OR 逻辑交互结构。

本仓库支持在不同算力预算下，对不同模型家族的交互行为进行结构化、可复现的对比分析。

本次首个公开版本（v1.0）支持以下模型对比：

- Qwen 2.5  
- DeepSeek-R1 蒸馏模型  

---

## 核心功能

- AND / OR 交互结构提取  
- 交互稀疏性分析  
- 可泛化交互分布分析  
- AND / OR 逻辑交互树构建  

---

## 支持的模型规模

### 小规模模式（1.5B 规模）

适用于算力受限环境。

| 模型 1 | 模型 2 |
|----------|----------|
| deepseek-r1-distill-qwen-1.5b | qwen2.5-1.5b |

运行方式：

    --model_size small

推荐场景：

- 消费级 GPU  
- 快速实验验证  
- 显存较小环境  

---

### 大规模模式（7B / 8B 规模）

默认配置。

| 模型 1 | 模型 2 |
|----------|----------|
| deepseek-r1-distill-llama-8b | qwen2.5-7b |

运行方式：

    --model_size large

推荐场景：

- 研究级实验  
- 完整交互结构分析  

---

## 安装说明

### 环境要求

- Python 3.10  
- Conda（推荐）  
- 支持 CUDA 的 GPU  

### 安装步骤

    conda create -n interaction python=3.10
    conda activate interaction
    cd Interaction_Explanation
    pip install -r requirements.txt

---

## 模型下载

模型会自动下载至：

    ./model_path

可在以下文件中修改模型路径：

    ./global_const

若已从 Hugging Face 下载模型，可放置于：

    ./model_path/hub/

---

## 快速开始

### 默认运行（大规模模式）

    python ./InteractionDemo

### 小规模模式示例

    python ./InteractionDemo --model_size small

---

## 命令行参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--gpu_id` | 1 | GPU 设备编号 |
| `--cal_batch_size` | 128 | 掩码前向计算批大小 |
| `--model_size` | large | small 或 large |

说明：如显存不足，请适当降低 `--cal_batch_size`。

---

## 自定义输入

若需运行自定义示例，请确保输入文件位于指定目录。

在创建自定义文件前，请先删除默认示例文件：

    rm datasets/custom-generation-test/sentences.txt
    rm -rf players/custom-generation-test/players-qwen-manual/*

---

### 句子要求

- 10–20 个单词  
- 不可重复  
- 需具备语义内容  

保存路径：

    datasets/custom-generation-test/sentences.txt

示例：

    echo "Even though he was a green hand, he still solved the" > datasets/custom-generation-test/sentences.txt
    echo "For months, we have urged China to change these unfair practices, and give fair and reciprocal treatment to American" >> datasets/custom-generation-test/sentences.txt

---

### Player 定义

创建 JSON 文件：

    players/custom-generation-test/player_words.json

示例：

    cat > players/custom-generation-test/player_words.json <<EOL
    {
        "0": ["Even","though","he","green","hand","he","still", "solved","the"],
        "1": [ "For months","urged", "China","change", "unfair practices,","give","fair","reciprocal","treatment","American"]
    }
    EOL

（可选）更多格式说明请参考：

    players/format_guide.txt

---

### 输入与 Player 约束说明

#### 1. 句子要求

- 最少：10 个单词  
- 最多：20 个单词  
- 超出范围将报错  
- 示例：
  - ✅ 合法："This is a sentence with exactly fifteen words, which meets the requirements."
  - ❌ 非法："This is short."
- 避免重复输入或重复短语：
  - ❌ 非法："Hello Hello Hello Hello Hello"

---

#### 2. Player 要求

- 最多 15 个  
- 最少 8 个  
- 必须按照原句出现顺序排列  
  - 示例句子：
    "Even though he was a green hand, he still solved the"
    - ✅ 合法：Even, though, he, was, ...
    - ❌ 非法：though, Even, was, he, ...
- 避免纯标点符号
  - ❌ 非法："!"
- 避免语义弱词（如介词、连词、冠词）
  - 不推荐：these, and, to 等
- 仅当单词由空格分隔时才视为有效 Player  
  - 例如：
    "doubt," 视为一个单词  
    "Hoppor's" 视为一个单词  
    "baby!)" 视为一个单词  

---

## 输出结构

每个模型生成目录：

    model_name#pretrain/

包含：

- generation.txt  
- inference.txt  
- interaction.txt  
- sparsity.png  
- interaction_tree.pdf  

两个模型之间的对比结果存储在：

    generalizable_interaction/

---

## 硬件建议

| 模式 | 推荐显存 |
|------|----------|
| small | ≥ 10GB |
| large | > 32GB |

---

## v1.0 版本范围

本版本重点包括：

- Qwen 与 DeepSeek 的交互结构对比  
- AND–OR 逻辑分解  
- 可泛化交互分析  

未来可能扩展：

- 更多模型家族  
- 更丰富的可视化工具  
- 计算流程优化  

---

## 贡献

欢迎提交 Issue 与 Pull Request。

提交问题时请包含：

- GPU 型号  
- CUDA 版本  
- 使用的模型规模  
- 完整报错日志  

---

## 许可证

Apache License 2.0
