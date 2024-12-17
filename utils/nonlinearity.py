import numpy as np
from .helpers import validate_and_pad_sbox

def sbox_to_binary_table(sbox):
    """
    Convert S-Box to binary truth table
    """
    table = []
    for value in sbox:
        table.append([int(bit) for bit in f"{value:08b}"])
    return np.array(table)

def compute_nonlinearity(sbox):
    """
    Compute the nonlinearity of the S-Box
    """
    # Validate and pad S-box
    sbox = validate_and_pad_sbox(sbox)

    binary_table = sbox_to_binary_table(sbox)
    num_inputs = len(sbox)
    input_bits = int(np.log2(num_inputs))
    max_bias = 0

    for coeff in range(1, 1 << input_bits):  # Exclude zero coefficient
        for output_bit in range(8):  # Check each output bit
            biases = []
            for x in range(num_inputs):
                dot_product = bin(coeff & x).count("1") % 2
                output_bit_value = binary_table[x, output_bit]
                bias = 1 if dot_product == output_bit_value else -1
                biases.append(bias)
            total_bias = abs(sum(biases))
            max_bias = max(max_bias, total_bias)

    # Compute nonlinearity
    nonlinearity = (1 << (input_bits - 1)) - max_bias // 2
    return nonlinearity

