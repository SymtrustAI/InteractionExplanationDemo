# Interaction Explanation
### Logical AND–OR Interaction Analysis for Large Language Models

[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)]()
[![CUDA](https://img.shields.io/badge/CUDA-Required-green.svg)]()
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)
[![Release](https://img.shields.io/badge/Release-v1.0-black.svg)]()
[![Status](https://img.shields.io/badge/Status-First%20Public%20Release-brightgreen.svg)]()

---

## Overview

**Interaction Explanation** is a research-oriented framework for extracting and analyzing logical AND–OR interactions inside Large Language Models (LLMs).

This repository enables structured and reproducible comparison of interaction behavior across model families under different computational budgets.

This first public release (v1.0) supports controlled comparison between:

- Qwen 2.5  
- DeepSeek-R1 distilled models  

---

## Key Features

- AND / OR interaction extraction  
- Interaction sparsity analysis  
- Generalizable interaction distribution analysis  
- AND / OR interaction tree construction  

---

## Supported Model Tiers

### Small Tier (1.5B Scale)

Designed for limited GPU environments.

| Model 1 | Model 2 |
|----------|----------|
| deepseek-r1-distill-qwen-1.5b | qwen2.5-1.5b |

Run with:

    --model_size small

Recommended for:

- Consumer GPUs  
- Rapid experimentation  
- Low-memory environments  

---

### Large Tier (7B / 8B Scale)

Default configuration.

| Model 1 | Model 2 |
|----------|----------|
| deepseek-r1-distill-llama-8b  | qwen2.5-7b |

Run with:

    --model_size large

Recommended for:

- Research-grade experiments  
- Full interaction analysis  

---

## Installation

### Requirements

- Python 3.10  
- Conda (recommended)  
- CUDA-capable GPU  

### Setup

    conda create -n interaction python=3.10
    conda activate interaction
    cd Interaction_Explanation
    pip install -r requirements.txt

---

## Model Download

Models are automatically downloaded to:

    ./model_path

You may modify the path in:

    ./global_const

If models are already downloaded from Hugging Face, place them under:

    ./model_path/hub/

---

## Quick Start

### Default Run (Large Tier)

    python ./InteractionDemo

### Small Tier Example

    python ./InteractionDemo --model_size small

---

## Command-Line Arguments

| Argument           | Default  | Description                     |
|--------------------|----------|---------------------------------|
| `--gpu_id`           | 1        | GPU device ID                  |
| `--cal_batch_size`   | 128      | Masked forward-pass batch size|
| `--model_size `      | large    | small or large                 |

Note: Reduce `--cal_batch_size` if GPU memory is limited.

---

## Custom Input
If you want to run your own example, please ensure that the required input files are in the specified directories:

**Note: before creating your own file, please remove the existing input files** 

```bash
rm datasets/custom-generation-test/sentences.txt
rm -rf players/custom-generation-test/players-qwen-manual/*
```

### Sentence Requirements

- 10–20 words  
- No repetition  
- Semantically meaningful content  

Save to:

    datasets/custom-generation-test/sentences.txt
   

For example:

```bash
echo "Even though he was a green hand, he still solved the" > datasets/custom-generation-test/sentences.txt
echo "For months, we have urged China to change these unfair practices, and give fair and reciprocal treatment to American" >> datasets/custom-generation-test/sentences.txt
```
---

### Player Definition

Create a JSON file named player_words.json and add content to it based on the required format:

    players/custom-generation-test/player_words.json

For example: 

```bash
cat > players/custom-generation-test/player_words.json <<EOL
{
    "0": ["Even","though","he","green","hand","he","still", "solved","the"],
    "1": [ "For months","urged", "China","change", "unfair practices,","give","fair","reciprocal","treatment","American"]
}
EOL
```
(Optional) For more details on formatting the JSON file, refer to players/format_guide.txt.
Constraints:

- 8–15 players  
- Preserve original token order  
- Avoid punctuation-only tokens  
- Avoid weak semantic tokens (e.g., and, to, the)  

---

**Guaidance on input sentence and player**

1. **Sentences**

- Minimum length: **10 words**
- Maximum length: **20 words**
- Sentences outside this range will be rejected with an error message.
- Example:
  - ✅ Valid: `"This is a sentence with exactly fifteen words, which meets the requirements."`
  - ❌ Invalid: `"This is short."`
- Avoid duplicate inputs or repeated phrases:
  - ❌ Invalid: `"Hello Hello Hello Hello Hello"`

2. **Players**

- maximum players: **15**
- minimum players: **8**
- Players must be in the order of appearance
  - Example: `"Even though he was a green hand, he still solved the"`
    - ✅ Valid: `Even`, `though`, `he`, `was`,  ...
    - ❌ Invalid:`though`,`Even`, `was`, `he`, ...
- Avoid pure punctutation
  - Example: `This is amazing !`
  - ❌ Invalid: `"!"`
- Avoid words without strong semantics
  - Words with weak semantics, such as prepositions, conjunctions, and articles, are suggested to be excluded.
  - Example: `For months, we have urged China to change these unfair practices, and give fair and reciprocal treatment to American`
    - words **NOT** recommended to be a player: `these`, `and`, `to`
- **Words are considered valid players only if they are separated by spaces**.
     - Example: "Without a doubt, one of Tobe Hoppor's best! Epic storytellng, great special effects, and The Spacegirl (vamp me baby!)."
          - "doubt," is considered a word, rather than "doubt"
          - "Hoppor's" is considered a word, rather than "Hoppor"
          - "baby!)" is considered a word, rather than "baby"
          
          
## Output Structure

Each model generates:

    model_name#pretrain/

Includes:

- generation.txt  
- inference.txt  
- interaction.txt  
- sparsity.png  
- interaction_tree.pdf  

Comparisoms between two models are stored in:

    generalizable_interaction/

---



## Hardware Recommendations

| Tier  | Suggested VRAM |
|-------|----------------|
| small | ≥ 10GB        |
| large | ≥ 32GB        |

---

## Scope of v1.0

This release focuses on:

- Qwen vs DeepSeek interaction comparison  
- AND–OR logical decomposition  
- Generalizable interaction analysis  

Future updates may include:

- Additional model families  
- Extended visualization tools  
- Pipeline optimization  

---

## Contributing

We welcome issues and pull requests.

When reporting issues, include:

- GPU type  
- CUDA version  
- Model tier  
- Full error logs  

---

## License

Apache License 2.0

