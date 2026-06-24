import os
import pandas as pd

# Importing our previously built modules
import entropy
import huffman
import lzw

def run_benchmark():
    """
    Runs the complete benchmark pipeline on all test files.
    Calculates Shannon Entropy, Huffman metrics, and LZW metrics.
    Exports the results to a CSV file.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    results_dir = os.path.join(base_dir, "results")
    
    # Ensure results directory exists
    os.makedirs(results_dir, exist_ok=True)
    
    files_to_test = [
        "text_sample.txt",
        "code_sample.py",
        "binary_sample.bin"
    ]
    
    results_matrix = []
    
    print("Starting automated benchmark pipeline. This may take a moment...\n")
    
    for file_name in files_to_test:
        file_path = os.path.join(data_dir, file_name)
        
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
            
            total_bytes = len(data)
            original_bits = total_bytes * 8
            
            if total_bytes == 0:
                continue
            
            # 1. Calculate Shannon Entropy
            freqs, _ = entropy.get_byte_frequencies(file_path)
            H = entropy.calculate_shannon_entropy(freqs, total_bytes)
            
            # 2. Calculate Huffman Coding Metrics
            root = huffman.build_huffman_tree(data)
            huff_codes = {}
            if root:
                # Handle single-character edge case
                if root.left is None and root.right is None:
                    huff_codes[root.byte_val] = "0"
                else:
                    huffman.generate_codes(root, "", huff_codes)
            
            huff_encoded_str = huffman.encode_data(data, huff_codes)
            huff_bits = len(huff_encoded_str)
            L_huff = huff_bits / total_bytes
            CR_huff = original_bits / huff_bits if huff_bits > 0 else 0
            
            # 3. Calculate LZW Metrics
            _, lzw_bits = lzw.lzw_encode(data)
            L_lzw = lzw_bits / total_bytes
            CR_lzw = original_bits / lzw_bits if lzw_bits > 0 else 0
            
            # 4. Append to Results Matrix
            results_matrix.append({
                "File_Name": file_name,
                "Size_Bytes": total_bytes,
                "Shannon_H": round(H, 4),
                "Huffman_L": round(L_huff, 4),
                "Huffman_CR": round(CR_huff, 4),
                "LZW_L": round(L_lzw, 4),
                "LZW_CR": round(CR_lzw, 4)
            })
            
        except FileNotFoundError:
            print(f"Error: Could not find '{file_name}' in the data folder.")
            
    # Create a pandas DataFrame for structured representation
    df = pd.DataFrame(results_matrix)
    
    # Display the table in the console
    print("=== Empirical Evaluation Matrix ===")
    print(df.to_string(index=False))
    print("===================================\n")
    
    # Save the DataFrame to a CSV file for Phase 7 (Visualization)
    csv_path = os.path.join(results_dir, "benchmark_results.csv")
    df.to_csv(csv_path, index=False)
    print(f"[SUCCESS] Results successfully exported to:\n{csv_path}")

if __name__ == "__main__":
    run_benchmark()