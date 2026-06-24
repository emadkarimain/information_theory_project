# Empirical Evaluation of Lossless Data Compression Algorithms
**Politecnico di Milano - MSc Telecommunication Engineering** **Course:** Information Theory  
**Authors:** Emad Karimianshamsabadi & Mahdi Soltani  

## Project Overview
This project provides a from-scratch, empirical evaluation of lossless data compression algorithms (Huffman Coding and LZW). It compares their practical performance (Average Code Length and Compression Ratio) against the theoretical lower bound defined by Shannon's Entropy.

## Data Sets Analyzed
To evaluate algorithmic behavior across different statistical distributions, we used:
1. **Natural Language Text:** High redundancy, predictable distribution.
2. **Source Code (Python):** Structured redundancy, repeated syntax/keywords.
3. **Binary/Random Data:** Uniform distribution, acting as an incompressible baseline.

## Project Structure
* `data/`: Contains the test files (`.txt`, `.py`, `.bin`).
* `src/`: Python source code modules (`entropy.py`, `huffman.py`, `lzw.py`, `benchmark.py`, `visualize.py`).
* `results/`: CSV exports of the empirical evaluation matrix.
* `figures/`: High-resolution academic plots generated via Matplotlib/Seaborn.

## How to Run
This project requires Python 3.11+.

1. **Activate Virtual Environment & Install Dependencies:**
```bash
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
```

2. **Run the Automated Benchmark:**
```bash
python src/benchmark.py
```
*This will calculate entropy, execute Huffman and LZW, and export the results to a CSV file.*

3. **Generate Academic Plots:**
```bash
python src/visualize.py
```
*This will read the CSV and generate comparative charts in the `figures/` directory.*