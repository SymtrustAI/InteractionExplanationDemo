# 🔍 Interaction Explanation  
### Interpretable AND–OR Interaction Analysis for Large Language Models  

**Startup Demo · Model Inference Transparency · Cross-Model Mechanistic Analysis**

[English](README.md) | [中文](README_zh.md)

![Python](https://img.shields.io/badge/Python-3.10-blue.svg)  
![CUDA](https://img.shields.io/badge/CUDA-Required-green.svg)  
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)  
![Release](https://img.shields.io/badge/Release-v1.0-black.svg)

---

## 🚀 Why This Matters

Large language models are powerful — but opaque.

**Interaction Explanation** reveals the logical interaction structure behind LLM inference.

Instead of only observing outputs, we analyze:

- 🧠 How tokens interact  
- 🌳 What interaction patterns emerge  
- 📊 Where interaction strength concentrates  
- ⚖ How inference logic differs across models  

This repository is a technical demonstration of SymTrustAI capability in LLM evalutaion and interpretability.

---

## 🧠 What We Demonstrate

### AND–OR Interaction Extraction  
Extract structured AND–OR interactions among input tokens.

### Interaction Sparsity Profiling  
Quantify the sparsity of interactions, demonstrating that a small subset of salient interactions is sufficient to faithfully explain an LLM’s inference logic.

### Logical Interaction Trees  
Construct interpretable AND–OR logical trees from salient interactions, capable of mimicking the model’s outputs across masked input prompts.

### Cross-Model Mechanistic Comparison  
Systematically compare interactions between DeepSeek and Qwen models to uncover differences in their underlying inference mechanisms.


---


## 🧪 Supported Configurations

### 🟢 Small Tier (1.5B)

| Model 1 | Model 2 |
|----------|----------|
| deepseek-r1-distill-qwen-1.5b | qwen2.5-1.5b |

Run:

    python ./demo --model_size small

Recommended for lightweight experimentation and limited GPU memory.

---

### 🔵 Large Tier (7B / 8B) — Default

| Model 1 | Model 2 |
|----------|----------|
| deepseek-r1-distill-llama-8b | qwen2.5-7b |

Run:

    python ./demo

Recommended for full structural analysis.

---

## ⚙ Installation

Requirements:

- Python 3.10  
- Conda  
- CUDA-capable GPU  

Setup:

    conda create -n interaction python=3.10
    conda activate interaction
    cd InteractionExplanationDemo
    pip install -r requirements.txt

---

## 🚀 Quick Start

Default:

    python ./demo

Small mode:

    python ./demo --model_size small

---

## 🛠 Command Line Arguments

| Argument | Default | Description |
|----------|----------|-------------|
| `--gpu_id` | 1 | GPU device ID |
| `--cal_batch_size` | 128 | Masked forward batch size |
| `--model_size` | large | small or large |

If GPU memory is limited, reduce `--cal_batch_size`.

---

## 📝 Custom Input (Advanced)

<details>
<summary><b>Click to expand configuration details</b></summary>

### Step 1 — Remove default example

    rm datasets/custom-generation-test/sentences.txt
    rm -rf players/custom-generation-test/players-qwen-manual/*

---

### Step 2 — Add sentences

Save to:

    datasets/custom-generation-test/sentences.txt

Constraints:

- 10–20 words  
- No repetition  
- Semantically meaningful  

---

### Step 3 — Define players

Create:

    players/custom-generation-test/player_words.json

Constraints:

- 8–15 players  
- Preserve original order  
- Avoid punctuation-only tokens  
- Avoid weak semantic words (e.g., and, to, the)

</details>


## 📊 Outputs

Each model produces:

- generation.txt  
- inference.txt  
- interaction.txt  
- sparsity.png  
- interaction_tree.pdf  

Cross-model comparison results are stored in:

    generalizable_interaction/

---

## 💻 Hardware Recommendations

| Tier | Recommended VRAM |
|------|------------------|
| small | ≥ 10GB |
| large | ≥ 32GB |

---

## 💡 Startup Vision

We believe interpretability is foundational for:

- Reliable AI systems  
- Safer deployment  
- Transparent model evaluation  
- Cross-model benchmarking  

This demo showcases our structural analysis capability.  
It does not expose internal production infrastructure.

---

## 📜 License

Apache License 2.0
