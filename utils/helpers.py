import numpy as np

def binary_representation(num, width):  
    """Convert number to binary with a fixed width."""  
    return [int(x) for x in f"{num:0{width}b}"]  

def to_bit_vector(value, length=8):  
    """Convert a value to a bit vector of specified length"""  
    return np.array([int(x) for x in f"{value:0{length}b}"])  

def hamming_weight(vec):  
    """Calculate the Hamming weight of a vector"""  
    return np.sum(vec)  

def validate_and_pad_sbox(sbox):
    """
    Validate and pad/truncate S-box to 256 elements
    
    Args:
        sbox (list): Input S-box
    
    Returns:
        list: Validated and padded/truncated S-box
    """
    # Ensure the S-box is padded to 256 elements if needed
    if len(sbox) < 256:
        # Pad with sequential values if the S-box is smaller
        sbox = sbox + list(range(len(sbox), 256))
    elif len(sbox) > 256:
        # Truncate to 256 elements if larger
        sbox = sbox[:256]
    
    return sbox

