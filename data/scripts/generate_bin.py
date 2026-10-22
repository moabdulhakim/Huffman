import json

# 1. Define the dummy input text
# 'a', 'b', 'c', 'd', and space will have standard Huffman codes.
# 'x', 'y', and 'z' will be treated as 'Others'.
dummy_text = "abaacaadaa xyz"

# 2. Hardcode the Huffman dictionary (Simulating Output of Member 1)
codes = {
    'a': '0',
    'b': '100',
    'c': '101',
    'd': '110',
    ' ': '1110',
    'Others': '1111'
}
others_list = ['x', 'y', 'z']

# 3. Simulate Member 2's encoding process
compressed_bits = ""
for char in dummy_text:
    if char in others_list:
        # Code for 'Others' + 8-bit ASCII representation of the character
        compressed_bits += codes['Others'] + format(ord(char), '08b')
    else:
        compressed_bits += codes[char]

# Calculate padding to make the bit string a multiple of 8
padding_length = (8 - (len(compressed_bits) % 8)) % 8
compressed_bits += "0" * padding_length

# Convert bit string to actual bytes
byte_array = bytearray()
for i in range(0, len(compressed_bits), 8):
    byte = compressed_bits[i:i+8]
    byte_array.append(int(byte, 2))

# Create the overhead JSON (Data needed for decompression)
overhead = json.dumps({'codes': codes, 'others': others_list})
overhead_bytes = overhead.encode('utf-8')
overhead_len = len(overhead_bytes)

# 4. Write to binary file according to the agreed Data Contract
# Contract Structure:
# - 4 bytes: Overhead Length (Big Endian)
# - N bytes: Overhead Data (JSON string)
# - 1 byte: Padding Length
# - M bytes: Compressed Binary Data
with open("dummy_compressed.bin", "wb") as f:
    f.write(overhead_len.to_bytes(4, byteorder='big'))
    f.write(overhead_bytes)
    f.write(padding_length.to_bytes(1, byteorder='big'))
    f.write(byte_array)

print("Generated dummy_compressed.bin successfully!")
print(f"Original Text: '{dummy_text}'")
print(f"Padding added: {padding_length} bits")
