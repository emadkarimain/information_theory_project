import heapq
import os
from collections import Counter

class HuffmanNode:
    """
    Represents a node in the Huffman Tree.
    """
    def __init__(self, byte_val: int | None, frequency: int):
        self.byte_val = byte_val
        self.frequency = frequency
        self.left: 'HuffmanNode' | None = None
        self.right: 'HuffmanNode' | None = None

    def __lt__(self, other: 'HuffmanNode'):
        # Required by heapq to prioritize nodes with lower frequencies
        return self.frequency < other.frequency

def build_huffman_tree(data: bytes) -> HuffmanNode | None:
    """
    Builds the Huffman tree using a priority queue (min-heap) and returns the root node.
    """
    if not data:
        return None

    frequencies = Counter(data)
    priority_queue = [HuffmanNode(byte_val, freq) for byte_val, freq in frequencies.items()]
    heapq.heapify(priority_queue)

    while len(priority_queue) > 1:
        left_node = heapq.heappop(priority_queue)
        right_node = heapq.heappop(priority_queue)

        # Create a merged internal node (byte_val is None for internal nodes)
        merged_node = HuffmanNode(None, left_node.frequency + right_node.frequency)
        merged_node.left = left_node
        merged_node.right = right_node

        heapq.heappush(priority_queue, merged_node)

    return priority_queue[0]

def generate_codes(node: HuffmanNode | None, current_code: str, codes: dict[int, str]):
    """
    Recursively traverses the Huffman tree to generate binary prefix codes.
    """
    if node is None:
        return

    # If it's a leaf node, assign the accumulated code
    if node.byte_val is not None:
        codes[node.byte_val] = current_code
        return

    generate_codes(node.left, current_code + "0", codes)
    generate_codes(node.right, current_code + "1", codes)

def encode_data(data: bytes, codes: dict[int, str]) -> str:
    """
    Encodes the original byte sequence into a continuous string of '0's and '1's.
    """
    return "".join(codes[byte_val] for byte_val in data)

def evaluate_huffman_performance(file_path: str):
    """
    Reads a file, applies Huffman coding, and calculates empirical metrics (L, CR).
    """
    file_name = os.path.basename(file_path)
    try:
        with open(file_path, 'rb') as f:
            data = f.read()

        if not data:
            print(f"File: {file_name:<20} | Status: Empty File")
            return

        original_bytes = len(data)
        original_bits = original_bytes * 8

        # 1. Build Tree and Generate Codes
        root = build_huffman_tree(data)
        codes = {}
        
        if root:
            # Handle edge case: file contains only one unique character
            if root.left is None and root.right is None:
                codes[root.byte_val] = "0"
            else:
                generate_codes(root, "", codes)

        # 2. Encode
        encoded_bit_string = encode_data(data, codes)
        encoded_bits_count = len(encoded_bit_string)

        # 3. Calculate Empirical Metrics
        empirical_L = encoded_bits_count / original_bytes
        # CR = Original Size / Compressed Size
        compression_ratio = original_bits / encoded_bits_count 

        print(f"File: {file_name:<20} | Orig. Size: {original_bytes:<6} B | "
              f"L: {empirical_L:.4f} bits/sym | CR: {compression_ratio:.4f}")

    except FileNotFoundError:
        print(f"Error: Could not find '{file_path}'. Please verify the data folder.")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")

    files_to_test = [
        "text_sample.txt",
        "code_sample.py",
        "binary_sample.bin"
    ]

    print("=== Huffman Coding Empirical Evaluation ===")
    for file_name in files_to_test:
        file_path = os.path.join(data_dir, file_name)
        evaluate_huffman_performance(file_path)
    print("===========================================")