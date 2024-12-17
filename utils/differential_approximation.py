import numpy as np
from .helpers import validate_and_pad_sbox

def calculate_dap(sbox):  
    """  
    Calculate Differential Approximation Probability (DAP)  
    """  
    # Validate and pad S-box
    sbox = validate_and_pad_sbox(sbox)
    
    n = len(sbox)  # S-box length  
    max_count = 0  

    # Iterate for each input difference (Δx)  
    for delta_x in range(1, n):  # Start from 1, as delta_x = 0 is not relevant  
        frequency_table = np.zeros(n, dtype=int)  

        for x in range(n):  
            # Calculate y1 and y2 for inputs with Δx difference  
            y1 = sbox[x]  
            y2 = sbox[x ^ delta_x]  
            delta_y = y1 ^ y2  # Output difference  
            frequency_table[delta_y] += 1  

        # Find maximum frequency for all Δy  
        max_frequency = np.max(frequency_table)  
        max_count = max(max_count, max_frequency)  

    # Calculate DAP (maximum probability)  
    dap_value = max_count / n  
    return dap_value  

