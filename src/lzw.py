import os

def lzw_encode(data: bytes) -> tuple[list[int], int]:
    """
    Encodes the input byte sequence using the LZW dictionary-based algorithm.
    Dynamically tracks the exact bit-length required for output codes to ensure
    accurate theoretical evaluation.
    
    Returns:
        A tuple containing the list of output codes and the exact total number of bits.
    """
    if not data:
        return [], 0

    # Initialize the base dictionary with all 256 single-byte characters
    dictionary = {bytes([i]): i for i in range(256)}
    dict_size = 256
    
    w = bytes()
    compressed_codes = []
    total_bits = 0
    
    # LZW dynamically increases code bit-length as the dictionary grows.
    # We start at 9 bits because our initial dictionary has 256 entries (needs 8 bits, 
    # so the new entries starting at 256 will require 9 bits).
    current_bit_length = 9 

    for k in data:
        c = bytes([k])
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            # Output the code for w
            compressed_codes.append(dictionary[w])
            total_bits += current_bit_length
            
            # Add wc to the dictionary
            dictionary[wc] = dict_size
            dict_size += 1
            
            # If dictionary size exceeds the maximum value representable by 
            # current_bit_length, we must increment the bit length.
            if dict_size > (1 << current_bit_length):
                current_bit_length += 1
                
            w = c
            
    # Output the code for the remaining sequence
    if w:
        compressed_codes.append(dictionary[w])
        total_bits += current_bit_length

    return compressed_codes, total_bits

def evaluate_lzw_performance(file_path: str):
    """
    Reads a file, applies LZW encoding, and calculates empirical metrics (L, CR).
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

        # Encode and get empirical bit count
        _, encoded_bits_count = lzw_encode(data)

        # Calculate Empirical Metrics
        empirical_L = encoded_bits_count / original_bytes
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

    print("=== LZW Algorithm Empirical Evaluation ===")
    for file_name in files_to_test:
        file_path = os.path.join(data_dir, file_name)
        evaluate_lzw_performance(file_path)
    print("==========================================")