from .helpers import validate_and_pad_sbox

def compute_differential_uniformity(sbox):
    """
    Compute the differential uniformity of the S-Box
    """
    # Validate and pad S-box
    sbox = validate_and_pad_sbox(sbox)
    num_inputs = len(sbox)
    max_diff_count = 0

    for input_diff in range(1, num_inputs):
        for output_diff in range(num_inputs):
            diff_count = 0
            for x in range(num_inputs):
                y1 = sbox[x]
                y2 = sbox[x ^ input_diff]
                
                if y1 ^ y2 == output_diff:
                    diff_count += 1
            
            max_diff_count = max(max_diff_count, diff_count)

    return max_diff_count

