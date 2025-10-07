# Token Optimizer: Pattern-Based Text Compression and Token Optimization

## Overview
Token Squeezer is a research-grade modular framework for pattern-based text compression. It detects structured entities in text (URLs, code snippets, emails, file paths, etc.), replaces them with placeholders, and quantifies savings in tokens and processing cost for large language models.
<img width="1567" height="763" alt="image" src="https://github.com/user-attachments/assets/c1dfaaf8-8c84-4d09-8286-8298471d399d" />
<img width="1592" height="774" alt="image" src="https://github.com/user-attachments/assets/7e6a77e0-6cd5-4204-90c3-39d6e1bbd3d6" />


## Modules
- **pattern_detector.py** – defines `PatternDetector` and `ContentType` taxonomy.
- **compression_engine.py** – performs compression and stores placeholder metadata.
- **restoration_engine.py** – restores text and verifies checksum integrity.
- **token_analytics.py** – computes per-sample and aggregate token/cost savings.
- **visualizations.py** – produces publication-quality figures for analysis.
- **main.py** – demonstrates usage with batch processing and visualization.

## Installation
```bash
git clone https://github.com/yourusername/token_squeezer.git
cd token_squeezer
pip install -r requirements.txt
```

## Requirements
Python ≥ 3.9, NumPy, Matplotlib, SciPy, Seaborn, Torch, Pandas

## Usage
Run demo:
```bash
python main.py
```

## Methodology
1. **Pattern Detection** — Regex-based multi-class pattern recognition.
2. **Compression** — Placeholder substitution with hash integrity checks.
3. **Restoration** — Integrity validation and checksum verification.
4. **Analysis** — Statistical summaries of token savings and cost reductions.
5. **Visualization** — Multi-panel plots showing compression distributions and cumulative savings.

## License
MIT License
