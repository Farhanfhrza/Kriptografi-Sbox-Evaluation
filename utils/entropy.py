import numpy as np

def compute_entropy(sbox):  
    """  
    Compute the entropy of the S-box  
    """  
    # Count frequency of each value  
    unique, counts = np.unique(sbox, return_counts=True)  
    probabilities = counts / len(sbox)  
    
    # Calculate Shannon entropy  
    entropy = -np.sum(probabilities * np.log2(probabilities))  
    
    # Normalized entropy (between 0 and 1)  
    max_possible_entropy = np.log2(len(unique))  
    normalized_entropy = entropy / max_possible_entropy  
    
    return {  
        'shannon_entropy': entropy,  
        'normalized_entropy': normalized_entropy  
    }

