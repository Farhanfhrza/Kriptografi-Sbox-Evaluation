
import streamlit as st
import pandas as pd
import numpy as np
import io

# Import all the utility functions
from utils.linear_approximation import linear_approximation_probability
from utils.nonlinearity import compute_nonlinearity, sbox_to_binary_table
from utils.differential_uniformity import compute_differential_uniformity
from utils.avalanche_criterion import strict_avalanche_criterion
from utils.differential_approximation import calculate_dap
from utils.entropy import compute_entropy
from utils.bit_independence import calculate_bic_sac, calculate_bic_nl

def main():
    st.title('Advanced S-box Cryptographic Analysis')
    
    # Sidebar for file upload
    st.sidebar.header('Import S-box')
    uploaded_file = st.sidebar.file_uploader(
        "Choose an Excel/CSV file", 
        type=['xlsx', 'xls', 'csv']
    )
    
    # Evaluation options with unique keys
    evaluation_options = st.sidebar.multiselect(  
        'Select Evaluation Metrics',  
        [  
            'Linear Approximation Probability (LAP)',   
            'Nonlinearity',   
            # 'Differential Uniformity',  
            # 'Binary Truth Table',  
            'Strict Avalanche Criterion (SAC)',  
            'Differential Approximation Probability (DAP)',  
            # 'Entropy Analysis',  
            'Bit Independence Criterion - SAC (BIC-SAC)',
            'Bit Independence Criterion - Nonlinearity (BIC-NL)'
        ],  
        default=['Linear Approximation Probability (LAP)'],  
        key='main_evaluation_metrics'  
    )  
    
    # Initialize session state for S-box
    if 'sbox' not in st.session_state:
        st.session_state.sbox = None
    
    try:
        # Read the uploaded file
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, header=None)
        else:
            df = pd.read_excel(uploaded_file, header=None)
        
        # Flatten the dataframe to a 1D list and convert to integers
        sbox = df.values.flatten().astype(int).tolist()
        
        # Validate and adjust S-box
        if len(sbox) < 256:
            st.warning(f"S-box size is {len(sbox)}. Padding to 256 elements.")
        elif len(sbox) > 256:
            st.warning(f"S-box size is {len(sbox)}. Truncating to 256 elements.")
        
        # Store S-box in session state
        st.session_state.sbox = sbox
        
        # Display S-box DataFrame  
        st.subheader('Imported S-box')  
        # Reshape the sbox into a 16x16 grid  
        sbox_grid = np.array(sbox).reshape(16, 16)  
        st.table(pd.DataFrame(sbox_grid,   
                            columns=[f'{i+1}' for i in range(16)],   
                            index=[f'{i+1}' for i in range(16)])  
        )  
        
        # Perform selected evaluations
        st.subheader('S-box Cryptographic Evaluation')
        
        # Linear Approximation Probability
        if 'Linear Approximation Probability (LAP)' in evaluation_options:
            lap_value = linear_approximation_probability(sbox)
            st.metric('Linear Approximation Probability (LAP)', f'{lap_value:.6f}')
        
        # Nonlinearity
        if 'Nonlinearity' in evaluation_options:
            nonlinearity = compute_nonlinearity(sbox)
            st.metric('Nonlinearity', str(nonlinearity))
        
        # # Differential Uniformity
        # if 'Differential Uniformity' in evaluation_options:
        #     diff_uniformity = compute_differential_uniformity(sbox)
        #     st.metric('Differential Uniformity', str(diff_uniformity))
        
        # # Binary Truth Table
        # if 'Binary Truth Table' in evaluation_options:
        #     binary_table = sbox_to_binary_table(sbox)
        #     st.subheader('Binary Truth Table')
        #     st.dataframe(pd.DataFrame(binary_table))

        # Strict Avalanche Criterion  
        if 'Strict Avalanche Criterion (SAC)' in evaluation_options:  
            sac_value = strict_avalanche_criterion(sbox)  
            st.metric('Strict Avalanche Criterion (SAC)', f'{sac_value:.10f}')  
        
        # Differential Approximation Probability  
        if 'Differential Approximation Probability (DAP)' in evaluation_options:  
            dap_value = calculate_dap(sbox)  
            st.metric('Differential Approximation Probability (DAP)', f'{dap_value:.10f}')  
        
        # Entropy Analysis  
        # if 'Entropy Analysis' in evaluation_options:  
        #     entropy_results = compute_entropy(sbox)  
        #     st.metric('Shannon Entropy', f'{entropy_results["shannon_entropy"]:.10f}')  
        #     st.metric('Normalized Entropy', f'{entropy_results["normalized_entropy"]:.10f}')

        # BIC-SAC  
        if 'Bit Independence Criterion - SAC (BIC-SAC)' in evaluation_options:  
            bic_sac_value = calculate_bic_sac(sbox)  
            st.metric('Bit Independence Criterion - SAC (BIC-SAC)', f'{bic_sac_value:.10f}')  
        
        # BIC-NL  
        if 'Bit Independence Criterion - Nonlinearity (BIC-NL)' in evaluation_options:  
            bic_nl_value = calculate_bic_nl(sbox)  
            st.metric('Bit Independence Criterion - Nonlinearity (BIC-NL)', str(bic_nl_value))    
        
        # Export option
        export_df = pd.DataFrame(sbox)
        export_buffer = io.BytesIO()
        export_df.to_excel(export_buffer, index=False, header=False)
        export_buffer.seek(0)
        
        st.download_button(
            label="Download S-box as Excel",
            data=export_buffer,
            file_name="sbox_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")

if __name__ == '__main__':
    main()

