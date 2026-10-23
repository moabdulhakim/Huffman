import json
def build_modified_huffman(text, min_limit):
    # This is a mock function simulating Member 1's output.
    # It returns hardcoded data for the test string "abaacaadaa xyz".
    # Member 2 can call this function to get the exact data types expected.
    
    # Dictionary containing the prefix codes for each symbol
    codes = {
        'a': '0',
        'b': '100',
        'c': '101',
        'd': '110',
        ' ': '1110',
        'Others': '1111'
    }
    
    # List containing symbols that fall under the 'Others' category
    others_list = ['x', 'y', 'z', '\n']
    
    return codes, others_list


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