<h1 align="center">Interaction Explanation</h1>

<p align="center">
  <a href="README.md">English</a> | 
  <a href="README_zh.md">中文</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10-blue.svg" />
  <img src="https://img.shields.io/badge/CUDA-Required-green.svg" />
  <a href="https://www.apache.org/licenses/LICENSE-2.0">
    <img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" />
  </a>
  <img src="https://img.shields.io/badge/Release-v1.0-black.svg" />
</p>



Recent theoretical advances suggest that well-trained deep neural networks (DNNs) can be faithfully explained by a sparse AND–OR logical model, which can mimic the network’s outputs across arbitrarily masked input configurations
Specifically, the AND–OR logical model is composed of interactions between subsets of input variables. 


- **AND interactions** capture AND relationships between input variables — all variables in a subset must be present to activate the effect.  
- **OR interactions** capture OR relationships between input variables — the presence of any variable in a subset can trigger the effect.


**Interaction Explanation** operationalizes this theory by extracting, quantifying, and visualizing these interactions within the AND-OR logical model, enabling structural analysis of LLM inference.


---

## Usage

### 🌐 Online Demo

One quick way to explore interaction-level analysis results is through our online demo platform.

The demo showcases real examples of AND–OR logical model explanations on `Qwen2.5-7B` and `deepseek-r1-distill-llama-8b`.  
It allows you to inspect how extracted interactions mechanistically explain detailed inference logic.  
You can also randomly mask input words to compare the AND–OR logical model’s output with the original LLM output.

👉 [Visit the Live Demo](https://www.symtrustai.com/demo)

👉 Prefer a guided walkthrough? Watch the platform demo above.

### 🎥 Platform Walkthrough

<p align="center">
<video width="720" controls>
  <source src="https://raw.githubusercontent.com/SymtrustAI/InteractionExplanationDemo/main/assets/Demo_walkthrough.mp4" type="video/mp4">
</video>
</p>

### 💻 Run Locally

**Small Tier** (1.5B): `deepseek-r1-distill-qwen-1.5b` vs `qwen2.5-1.5b`

Run: `python ./demo --model_size small`


**Large Tier** (7B / 8B) — Default:`deepseek-r1-distill-llama-8b` vs `qwen2.5-7b`


Run: `python ./demo`


##Installation

Requirements:

- Python 3.10  
- Conda  
- CUDA-capable GPU  

Setup:

    conda create -n interaction python=3.10
    conda activate interaction
    cd InteractionExplanationDemo
    pip install -r requirements.txt



## Model Setup

Models are automatically downloaded and saved to:`./model_path`

You can modify the default model directory in:`./global_const`

If you have already downloaded models from Hugging Face, place them under:`./model_path/hub/`

**The framework will automatically detect and load the models from this location.**



## Command Line Arguments

| Argument | Default | Description |
|----------|----------|-------------|
| `--gpu_id` | 1 | GPU device ID |
| `--cal_batch_size` | 128 | Masked forward batch size |
| `--model_size` | large | small or large |

If GPU memory is limited, reduce `--cal_batch_size`.



## Custom Input (Advanced)

<details>
<summary><b>Click to expand configuration details</b></summary>

### Step 1 — Remove default example

    rm datasets/custom-generation-test/sentences.txt
    rm -rf players/custom-generation-test/players-qwen-manual/*



### Step 2 — Add sentences

Save to:

    datasets/custom-generation-test/sentences.txt

Constraints:

- 10–20 words  
- No repetition  
- Semantically meaningful  



### Step 3 — Define players

Create:

    players/custom-generation-test/player_words.json

Constraints:

- 8–15 players  
- Preserve original order  
- Avoid punctuation-only tokens  
- Avoid weak semantic words (e.g., and, to, the)

</details>


## Outputs

Each model produces:

- generation.txt  
- inference.txt  
- interaction.txt  
- sparsity.png  
- interaction_tree.pdf  

Cross-model comparison results are stored in: `generalizable_interaction/`



## Hardware Recommendations

| Tier | Recommended VRAM |
|------|------------------|
| small | > 10GB |
| large | > 32GB |




## License

Apache License 2.0
