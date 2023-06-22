import pandas as pd
import numpy as np

def add_missing_columns(df):
    desired_columns = ['sample_number', 'sample_type','code', 'description','kind', 'date_sampled', 'date_received',
                       'date_printed', 'ST', 'CO', 'institution','address1','address2', 'investigator', 'comments']
    
    existing_columns = df.columns.tolist()
    missing_columns = list(set(desired_columns) - set(existing_columns))
    
    for column in missing_columns:
        if column in ['sample_type', 'description']:
            df[column] = 'None'
        elif column.startswith('date_'):
            df[column] = pd.to_datetime('01/01/2001', format='%d/%m/%Y')
        else:
            df[column] = 'None'
    
    return df[desired_columns]

# Example usage

if __name__ == "__main__":
    input_dataframe = pd.DataFrame({
        'sample_number': [1, 2, 3],
        'description': ['Sample A', 'Sample B', 'Sample C'],
        'ST': ['ST1', 'ST2', 'ST3'],
        'institution': ['Inst1', 'Inst2', 'Inst3']
    })

    output_dataframe = add_missing_columns(input_dataframe)
    print(output_dataframe)