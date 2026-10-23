import argparse
import heapq
import json
from collections import Counter


class Node:

  def __init__(self, char, freq):
    self.char = char
    self.freq = freq
    self.left = None
    self.right = None

  def __lt__(self, other):
    return self.freq < other.freq


def build_modified_huffman(text, limit=None):
  if not text:
    return {}, [], None

  freq_map = Counter(text)
  others_list = []

  if limit and len(freq_map) > limit:
    sorted_freq = sorted(freq_map.items(), key=lambda x: x[1])
    num_others = len(freq_map) - limit + 1
    others_tuples = sorted_freq[:num_others]
    others_list = [char for char, _ in others_tuples]
    others_total_freq = sum(freq for _, freq in others_tuples)

    new_freq_map = {
        char: freq for char, freq in sorted_freq[num_others:]
    }
    new_freq_map["Others"] = others_total_freq
    freq_map = new_freq_map

  heap = [Node(char, freq) for char, freq in freq_map.items()]
  heapq.heapify(heap)

  if len(heap) == 1:
    root = Node(None, heap[0].freq)
    root.left = heap[0]
    return {heap[0].char: "0"}, others_list, root

  while len(heap) > 1:
    left = heapq.heappop(heap)
    right = heapq.heappop(heap)

    merged = Node(None, left.freq + right.freq)
    merged.left = left
    merged.right = right

    heapq.heappush(heap, merged)

  root = heap[0]
  huffman_codes = {}

  def generate_codes(node, current_code):
    if node is None:
      return
    if node.char is not None:
      huffman_codes[node.char] = current_code
      return
    generate_codes(node.left, current_code + "0")
    generate_codes(node.right, current_code + "1")

  generate_codes(root, "")
  return huffman_codes, others_list


def compress(input_file, output_file, min_limit):
    with open(input_file, 'r') as file:
        content = file.read()

    if not content:
        print("Input file is empty.")
        return
    
    codes, others_list = build_modified_huffman(content, min_limit)

    compressed_bits = ""

    for char in content:
        if char not in others_list:
            compressed_bits += codes[char]
        else:
            compressed_bits += codes['Others'] + format(ord(char), '08b')

    padding_len = 8 - (len(compressed_bits) % 8)
    compressed_bits += '0' * padding_len
    padding_info = format(padding_len, '08b')
    compressed_bits = padding_info + compressed_bits

    byte_array = bytearray()
    for i in range(0, len(compressed_bits), 8):
        byte = compressed_bits[i:i + 8]
        byte_array.append(int(byte, 2))


    overhead = json.dumps({
        'codes': codes,
        'others': others_list
    })
    overhead_bytes = overhead.encode('utf-8')
    overhead_len = len(overhead_bytes)

    with open(output_file, 'wb') as file:
        file.write(overhead_len.to_bytes(4, byteorder='big'))
        file.write(overhead_bytes)
        file.write(byte_array)
    
    print(f"Compression complete. Output written to {output_file}.")


def decompress(input_file, output_file):
    with open(input_file, 'rb') as f:
        data = f.read()

    overhead_len = int.from_bytes(data[0:4], byteorder='big')

    overhead_bytes = data[4:4 + overhead_len]
    overhead = json.loads(overhead_bytes.decode('utf-8'))
    codes = overhead['codes']
    others_list = overhead['others']

    code_to_char = {code: char for char, code in codes.items()}
    others_code = codes.get('Others')

    rest = data[4 + overhead_len:]

    padding_len = rest[0]

    compressed_bytes = rest[1:]

    bits = ''.join(format(byte, '08b') for byte in compressed_bytes)
    if padding_len:
        bits = bits[:-padding_len]

    output_chars = []
    i = 0
    n = len(bits)
    while i < n:
        current = ''
        matched = False
        for j in range(i, n):
            current += bits[j]
            if others_code is not None and current == others_code:
                byte_bits = bits[j + 1:j + 9]
                output_chars.append(chr(int(byte_bits, 2)))
                i = j + 9
                matched = True
                break
            elif current in code_to_char:
                output_chars.append(code_to_char[current])
                i = j + 1
                matched = True
                break
        if not matched:
            raise ValueError("Corrupt data: no matching Huffman code found")

    content = ''.join(output_chars)

    with open(output_file, 'w') as f:
        f.write(content)

    print(f"Decompression complete. Output written to {output_file}.")

    
def main():
  parser = argparse.ArgumentParser()
  group = parser.add_mutually_exclusive_group(required=True)
  group.add_argument("-c", "--compress", action="store_true")
  group.add_argument("-d", "--decompress", action="store_true")

  parser.add_argument("-i", "--input", required=True, type=str)
  parser.add_argument("-o", "--output", type=str)
  parser.add_argument("-l", "--limit", type=int, default=None)

  args = parser.parse_args()

  if args.compress:
    if not args.input:
        print("Input file is required for compression. use -i <input_file> to specify the input file.")
        return

    compress(args.input, args.output or f"{args.input}.compressed.bin", args.limit)

  elif args.decompress:
    if not args.input:
        print("Input file is required for decompression. use -i <input_file> to specify the input file.")
        return

    output_file = args.output
    if not output_file:
        base = args.input
        for suffix in (".compressed.bin", ".bin"):
            if base.endswith(suffix):
                base = base[: -len(suffix)]
                break
        output_file = f"{base}.decompressed.txt"

    decompress(args.input, args.output or output_file)


if __name__ == "__main__":
  main()