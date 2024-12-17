from .helpers import validate_and_pad_sbox

def linear_approximation_probability(sbox):
    """
    Calculate the Linear Approximation Probability (LAP) for an S-box.
    """
    # Validate and pad S-box
    sbox = validate_and_pad_sbox(sbox)

    max_lap = 0  # Maximum LAP value

    # Iterate over all non-zero input and output masks
    for input_mask in range(1, 256):
        for output_mask in range(1, 256):
            count = 0

            # Check all input-output pairs
            for x in range(256):
                input_parity = bin(x & input_mask).count('1') % 2
                output_parity = bin(sbox[x] & output_mask).count('1') % 2

                if input_parity == output_parity:
                    count += 1

            # Calculate the probability and normalize it
            lap = abs(count - 128) / 128
            max_lap = max(max_lap, lap)

    return max_lap / 2  # LAP normalized to 0.5 for cryptographic analysis

