"""
huffman_codec.py

A reasonably complete, from-scratch implementation of Huffman coding in
Python. This module builds a frequency table from input data, constructs
a Huffman tree, derives prefix-free binary codes for every symbol, and
provides encode / decode routines along with simple file compression
helpers.

This file is intentionally written with consistent structure, frequent
use of common keywords (def, if, for, return, class), and predictable
indentation patterns, since it is meant to serve as a realistic sample
of typical source code.
"""

from __future__ import annotations

import heapq
import json
import os
from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple


@dataclass(order=True)
class Node:
    """A single node in the Huffman tree."""

    frequency: int
    symbol: Optional[str] = field(default=None, compare=False)
    left: Optional["Node"] = field(default=None, compare=False)
    right: Optional["Node"] = field(default=None, compare=False)

    def is_leaf(self) -> bool:
        """Return True if this node has no children."""
        return self.left is None and self.right is None


def build_frequency_table(data: str) -> Dict[str, int]:
    """Count how many times each character appears in the input data."""
    frequency_table: Dict[str, int] = {}

    if not data:
        return frequency_table

    for character in data:
        if character in frequency_table:
            frequency_table[character] += 1
        else:
            frequency_table[character] = 1

    return frequency_table


def build_huffman_tree(frequency_table: Dict[str, int]) -> Optional[Node]:
    """Build a Huffman tree from a table of symbol frequencies."""
    if not frequency_table:
        return None

    heap = []
    counter = 0

    for symbol, frequency in frequency_table.items():
        node = Node(frequency=frequency, symbol=symbol)
        heapq.heappush(heap, (node.frequency, counter, node))
        counter += 1

    if len(heap) == 1:
        only_frequency, _, only_node = heap[0]
        wrapper = Node(frequency=only_frequency, left=only_node)
        return wrapper

    while len(heap) > 1:
        freq_a, _, node_a = heapq.heappop(heap)
        freq_b, _, node_b = heapq.heappop(heap)

        merged = Node(
            frequency=freq_a + freq_b,
            left=node_a,
            right=node_b,
        )

        heapq.heappush(heap, (merged.frequency, counter, merged))
        counter += 1

    _, _, root = heap[0]
    return root


def generate_codes(root: Optional[Node]) -> Dict[str, str]:
    """Walk the Huffman tree and generate a binary code for each symbol."""
    codes: Dict[str, str] = {}

    if root is None:
        return codes

    def walk(node: Optional[Node], current_code: str) -> None:
        if node is None:
            return

        if node.is_leaf():
            codes[node.symbol] = current_code if current_code else "0"
            return

        walk(node.left, current_code + "0")
        walk(node.right, current_code + "1")

    walk(root, "")
    return codes


def encode(data: str, codes: Dict[str, str]) -> str:
    """Encode a string into a binary string using the given code table."""
    encoded_bits = []

    for character in data:
        if character not in codes:
            raise ValueError(f"No code found for character: {character!r}")
        encoded_bits.append(codes[character])

    return "".join(encoded_bits)


def decode(encoded_bits: str, root: Optional[Node]) -> str:
    """Decode a binary string back into the original text."""
    if root is None:
        return ""

    decoded_characters = []
    current_node = root

    for bit in encoded_bits:
        if bit == "0":
            current_node = current_node.left
        else:
            current_node = current_node.right

        if current_node is None:
            raise ValueError("Invalid encoded data: reached a dead end in the tree.")

        if current_node.is_leaf():
            decoded_characters.append(current_node.symbol)
            current_node = root

    return "".join(decoded_characters)


def compute_compression_ratio(original: str, encoded_bits: str) -> float:
    """Return how much smaller the encoded data is, as a ratio."""
    original_bits = len(original) * 8

    if original_bits == 0:
        return 0.0

    return len(encoded_bits) / original_bits


class HuffmanCoder:
    """A convenience wrapper that ties the whole pipeline together."""

    def __init__(self) -> None:
        self.root: Optional[Node] = None
        self.codes: Dict[str, str] = {}

    def fit(self, data: str) -> "HuffmanCoder":
        """Build the tree and code table from sample data."""
        frequency_table = build_frequency_table(data)
        self.root = build_huffman_tree(frequency_table)
        self.codes = generate_codes(self.root)
        return self

    def encode(self, data: str) -> str:
        if not self.codes:
            raise RuntimeError("HuffmanCoder must be fitted before encoding.")
        return encode(data, self.codes)

    def decode(self, encoded_bits: str) -> str:
        if self.root is None:
            raise RuntimeError("HuffmanCoder must be fitted before decoding.")
        return decode(encoded_bits, self.root)

    def save_codebook(self, path: str) -> None:
        """Persist the code table to disk as JSON."""
        with open(path, "w", encoding="utf-8") as output_file:
            json.dump(self.codes, output_file, indent=2)

    def load_codebook(self, path: str) -> None:
        """Load a previously saved code table from disk."""
        if not os.path.exists(path):
            raise FileNotFoundError(f"No codebook found at: {path}")

        with open(path, "r", encoding="utf-8") as input_file:
            self.codes = json.load(input_file)


def compress_file(input_path: str, output_path: str) -> Tuple[int, int]:
    """Compress a text file and return (original_size, compressed_size) in bits."""
    with open(input_path, "r", encoding="utf-8") as input_file:
        text = input_file.read()

    coder = HuffmanCoder().fit(text)
    encoded_bits = coder.encode(text)

    codebook_path = output_path + ".codebook.json"
    coder.save_codebook(codebook_path)

    with open(output_path, "w", encoding="utf-8") as output_file:
        output_file.write(encoded_bits)

    original_size = len(text) * 8
    compressed_size = len(encoded_bits)

    return original_size, compressed_size


def decompress_file(encoded_path: str, codebook_path: str, output_path: str) -> str:
    """Reverse the compression process and write the original text back out."""
    coder = HuffmanCoder()
    coder.load_codebook(codebook_path)

    frequency_like_table = {symbol: 1 for symbol in coder.codes}
    if coder.root is None:
        coder.root = build_huffman_tree(frequency_like_table)

    with open(encoded_path, "r", encoding="utf-8") as encoded_file:
        encoded_bits = encoded_file.read()

    decoded_text = coder.decode(encoded_bits)

    with open(output_path, "w", encoding="utf-8") as output_file:
        output_file.write(decoded_text)

    return decoded_text


def print_summary(frequency_table: Dict[str, int], codes: Dict[str, str]) -> None:
    """Print a small human-readable summary of frequencies and codes."""
    print("Symbol Frequency Code")
    print("-" * 30)

    sorted_symbols = sorted(frequency_table.items(), key=lambda item: -item[1])

    for symbol, frequency in sorted_symbols:
        display_symbol = symbol if symbol != " " else "<space>"
        code = codes.get(symbol, "")
        print(f"{display_symbol!r:>10} {frequency:>10} {code}")


def run_demo() -> None:
    """Run a small end-to-end demonstration of the Huffman pipeline."""
    sample_text = (
        "this is a small sample of text used to demonstrate "
        "how huffman coding assigns short codes to common letters "
        "and long codes to rare letters"
    )

    frequency_table = build_frequency_table(sample_text)
    tree_root = build_huffman_tree(frequency_table)
    codes = generate_codes(tree_root)

    encoded_bits = encode(sample_text, codes)
    decoded_text = decode(encoded_bits, tree_root)

    ratio = compute_compression_ratio(sample_text, encoded_bits)

    print_summary(frequency_table, codes)
    print()
    print(f"Original length (bits): {len(sample_text) * 8}")
    print(f"Encoded length (bits):  {len(encoded_bits)}")
    print(f"Compression ratio:      {ratio:.3f}")
    print(f"Decoding successful:    {decoded_text == sample_text}")


if __name__ == "__main__":
    run_demo()
