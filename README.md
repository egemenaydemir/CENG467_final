# Text-to-SQL in The Medical Domain

## Project
This repository provides tools for training, preprocessing, and evaluating EHRSQL-based models that generate SQL queries from clinical text and evaluate them with standard metrics.

## Installation
1. Create and activate a conda environment:

```bash
conda create -n ehrsql python=3.9 -y
conda activate ehrsql
```

2. Install the project dependencies:

```bash
pip install -r requirements.txt
```

Note: If you need a specific CUDA-enabled `torch` build, follow the official instructions at https://pytorch.org/get-started/locally/ to install `torch` first, then run:

```bash
pip install -r requirements.txt --no-deps
```

## Data (EHRSQL)
The EHRSQL dataset and SQL databases are NOT included in this repository. To obtain them, clone the original EHRSQL repository:

```bash
git clone https://github.com/glee4810/EHRSQL.git
```

Place the `EHRSQL` directory at the project root (the repository's `.gitignore` excludes it to avoid committing large data files).

## Repository structure (current, simplified)
```
final_CENG467/
	README.md
	requirements.txt
	.gitignore
	dataset_info.py
	dataset_info.csv
	EHRSQL/                # external, not committed
	EHRSQL/dataset/        # expected dataset files (train/valid/test)
	EHRSQL/eicu/           # example subfolder in EHRSQL
	EHRSQL/mimic_iii/      # example subfolder in EHRSQL
	EHRSQL/*.sql           # sqlite DB files (not committed)
	EHRSQL/outputs/        # evaluation outputs (local)
	T5/                    # model and training code
	utils/
	preprocess/
```
