
import streamlit as st
import pandas as pd
import numpy as np
import io
import re

def sanitize_sheet_name(name, max_length=31):
    """
    Sanitize sheet name to be Excel-compatible
    
    Parameters:
    - name: Original sheet name
    - max_length: Maximum allowed length (default 31)
    
    Returns:
    - Sanitized sheet name
    """
    # Remove special characters
    sanitized = re.sub(r'[^\w\s-]', '', name)
    
    # Replace spaces with underscores
    sanitized = sanitized.replace(' ', '_')
    
    # Truncate to max length
    return sanitized[:max_length]

def create_sbox_table(sbox):
    """
    Convert 1D S-box to 16x16 DataFrame
    
    Parameters:
    - sbox: 1D list of S-box values
    
    Returns:
    - DataFrame representing 16x16 S-box table
    """
    # Ensure the S-box is exactly 256 elements
    if len(sbox) != 256:
        raise ValueError("S-box must contain exactly 256 elements")
    
    # Reshape into 16x16 grid
    sbox_grid = np.array(sbox).reshape(16, 16)
    
    # Create DataFrame with labeled rows and columns
    sbox_df = pd.DataFrame(
        sbox_grid, 
        columns=[f'{i+1}' for i in range(16)],
        index=[f'{i+1}' for i in range(16)]
    )
    
    return sbox_df

def create_downloadable_excel(data, sheet_name='Sheet1', filename='sbox_evaluation.xlsx'):
    """
    Create a downloadable Excel file from various data types
    
    Parameters:
    - data: Can be a dictionary of DataFrames, a single DataFrame, or a list/array
    - sheet_name: Name of the sheet if single DataFrame
    - filename: Name of the downloaded file
    
    Returns:
    - Streamlit download button
    """
    # Create a buffer to store the Excel file
    buffer = io.BytesIO()
    
    # Handle different input types
    try:
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            if isinstance(data, dict):
                # Multiple sheets in a workbook
                for sheet, df in data.items():
                    # Sanitize sheet name
                    safe_sheet_name = sanitize_sheet_name(str(sheet))
                    
                    # Convert to DataFrame if not already
                    if not isinstance(df, pd.DataFrame):
                        df = pd.DataFrame(df)
                    
                    # Write to Excel with sanitized sheet name
                    df.to_excel(writer, sheet_name=safe_sheet_name, index=True)
            
            elif isinstance(data, pd.DataFrame):
                # Single DataFrame
                data.to_excel(writer, sheet_name=sanitize_sheet_name(sheet_name), index=True)
            
            elif isinstance(data, (list, np.ndarray)):
                # Convert list or array to DataFrame
                df = pd.DataFrame(data)
                df.to_excel(writer, sheet_name=sanitize_sheet_name(sheet_name), index=True)
            
            else:
                st.error("Unsupported data type for Excel conversion")
                return None
    
    except Exception as e:
        st.error(f"Error creating Excel file: {e}")
        return None

    # Seek to the beginning of the buffer
    buffer.seek(0)
    
    # Create Streamlit download button
    return st.download_button(
        label="Download Evaluation Results (Excel)",
        data=buffer,
        file_name=filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

def prepare_sbox_evaluation_download(sbox, evaluation_results):
    """
    Prepare a comprehensive Excel file with S-box evaluation results
    
    Parameters:
    - sbox: The S-box list
    - evaluation_results: Dictionary of evaluation metrics and their results
    
    Returns:
    - Downloadable Excel file with multiple sheets
    """
    # Prepare data for Excel export
    export_data = {
        'SBox_16x16_Table': create_sbox_table(sbox),
    }
    
    # Add evaluation results to export data
    for metric, value in evaluation_results.items():
        if metric == 'S-box':
            continue  # Skip duplicate S-box sheet
        
        if isinstance(value, (int, float)):
            # Scalar values
            export_data[f'{metric}_Value'] = pd.DataFrame([value], columns=['Value'])
        elif isinstance(value, (list, np.ndarray)):
            # Matrices or lists
            export_data[f'{metric}_Matrix'] = pd.DataFrame(
                value, 
                columns=[f'{i+1}' for i in range(len(value[0]))],
                index=[f'{i+1}' for i in range(len(value))]
            )
        elif isinstance(value, dict):
            # For more complex results
            for sub_metric, sub_value in value.items():
                export_data[f"{metric}_{sub_metric}"] = pd.DataFrame([sub_value], columns=['Value'])
    
    # Create downloadable Excel
    return create_downloadable_excel(
        export_data, 
        filename='sbox_cryptographic_evaluation.xlsx'
    )

def add_download_buttons(sbox, evaluation_options, sbox_results):
    """
    Add download buttons for S-box evaluation results
    
    Parameters:
    - sbox: The S-box list
    - evaluation_options: List of selected evaluation metrics
    - sbox_results: Dictionary to store evaluation results
    """
    # Prepare results for download
    download_results = {}
    
    # Collect results based on selected options
    if 'Linear Approximation Probability (LAP)' in evaluation_options:
        download_results['LAP'] = sbox_results.get('lap', None)
    
    if 'Nonlinearity' in evaluation_options:
        download_results['Nonlinearity'] = sbox_results.get('nonlinearity', None)
    
    if 'Strict Avalanche Criterion (SAC)' in evaluation_options:
        download_results['SAC_Value'] = sbox_results.get('sac_value', None)
        download_results['SAC_Matrix'] = sbox_results.get('sac_matrix', None)
    
    if 'Differential Approximation Probability (DAP)' in evaluation_options:
        download_results['DAP'] = sbox_results.get('dap', None)
    
    if 'Bit Independence Criterion - SAC (BIC-SAC)' in evaluation_options:
        download_results['BIC_SAC'] = sbox_results.get('bic_sac', None)
    
    if 'Bit Independence Criterion - Nonlinearity (BIC-NL)' in evaluation_options:
        download_results['BIC_NL'] = sbox_results.get('bic_nl', None)
    
    # Create download button
    return prepare_sbox_evaluation_download(sbox, download_results)

