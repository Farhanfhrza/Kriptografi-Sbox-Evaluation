import numpy as np
from itertools import product
from .helpers import to_bit_vector, hamming_weight, validate_and_pad_sbox

def calculate_bic_sac(sbox):  
    """  
    Calculate the Bit Independence Criterion - Strict Avalanche Criterion (BIC-SAC)  
    
    Args:  
        sbox (list): Input S-box  
    
    Returns:  
        float: BIC-SAC value  
    """  
    # Validate and pad S-box
    sbox = validate_and_pad_sbox(sbox)
    
    n = len(sbox)  
    total_bits = len(format(n - 1, 'b'))  # Bit length (8 for GF(2^8))  
    bic_sac_values = []  

    # Loop for each output bit pair  
    for i in range(total_bits):  # Input bit to flip  
        for j1 in range(total_bits):  # First output bit  
            for j2 in range(total_bits):  # Second output bit  
                if j1 != j2:  # Only for different output bits  
                    diff_count = 0  
                    for x in range(n):  
                        flipped_x = x ^ (1 << i)  # Flip the i-th input bit  
                        bit_j1 = (sbox[x] >> j1) & 1  # j1 bit of original output  
                        bit_j2 = (sbox[x] >> j2) & 1  # j2 bit of original output  
                        flipped_bit_j1 = (sbox[flipped_x] >> j1) & 1  # j1 bit of flipped output  
                        flipped_bit_j2 = (sbox[flipped_x] >> j2) & 1  # j2 bit of flipped output  
                        diff_count += (bit_j1 ^ flipped_bit_j1) ^ (bit_j2 ^ flipped_bit_j2)  # XOR differences  
                    bic_sac_values.append(diff_count / n)  # Normalize for bit pair  
    
    return sum(bic_sac_values) / len(bic_sac_values)  # Average of all bit pairs  

def calculate_bic_nl(sbox):  
    """  
    Calculate the Bit Independence Criterion - Nonlinearity (BIC-NL)  
    
    Args:  
        sbox (list): Input S-box  
    
    Returns:  
        int: Minimum distance from affine functions  
    """  
    # Validate and pad S-box
    sbox = validate_and_pad_sbox(sbox)
    
    n = 8  # Input length  
    m = 8  # Output length  
    min_distance = float("inf")  

    # Convert S-box to boolean function table  
    truth_table = np.array([to_bit_vector(sbox[x]) for x in range(256)])  

    # Create all affine functions  
    affine_masks = list(product([0, 1], repeat=n))  

    for mask in affine_masks:  
        mask = np.array(mask)  
        for const in [0, 1]:  
            affine_output = np.array([hamming_weight(mask & to_bit_vector(x)) % 2 ^ const for x in range(256)])  
            for bit in range(m):  # For each output bit of boolean function  
                f_bit = truth_table[:, bit]  
                distance = 256 - np.sum(f_bit == affine_output)  
                min_distance = min(min_distance, distance)  

    return min_distance  

