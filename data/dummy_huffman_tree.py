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
    others_list = ['x', 'y', 'z']
    
    return codes, others_list
