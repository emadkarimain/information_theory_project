import math
import os
from collections import Counter

def get_byte_frequencies(file_path: str) -> tuple[dict, int]:
    """
    Reads a file in binary mode and returns a dictionary of byte frequencies
    along with the total number of bytes.
    """
    with open(file_path, 'rb') as f:
        data = f.read()
    return dict(Counter(data)), len(data)

def calculate_shannon_entropy(frequencies: dict, total_symbols: int) -> float:
    """
    Calculates the Shannon entropy based on symbol frequencies.
    Formula: H(X) = - sum( p(x) * log2(p(x)) )
    """
    entropy = 0.0
    for count in frequencies.values():
        probability = count / total_symbols
        entropy -= probability * math.log2(probability)
    return entropy

def analyze_file_entropy(file_path: str) -> float:
    """
    Helper function to process a file, calculate its entropy,
    and print the results to the console.
    """
    file_name = os.path.basename(file_path)
    try:
        frequencies, total_bytes = get_byte_frequencies(file_path)
        
        if total_bytes == 0:
            print(f"File: {file_name:<20} | Status: Empty File")
            return 0.0
        
        entropy = calculate_shannon_entropy(frequencies, total_bytes)
        unique_symbols = len(frequencies)
        
        print(f"File: {file_name:<20} | Size: {total_bytes:<8} bytes | "
              f"Unique Symbols: {unique_symbols:<3}/256 | Entropy: {entropy:.4f} bits/symbol")
        
        return entropy
    except FileNotFoundError:
        print(f"Error: Could not find '{file_path}'. Please check the data folder.")
        return 0.0

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    
    files_to_test = [
        "text_sample.txt",
        "code_sample.py",
        "binary_sample.bin"
    ]
    
    print("=== Shannon Entropy Baseline Analysis ===")
    for file_name in files_to_test:
        file_path = os.path.join(data_dir, file_name)
        analyze_file_entropy(file_path)
    print("=========================================")