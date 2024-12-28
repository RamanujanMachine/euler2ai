import pickle
import pandas as pd
import sympy as sp


# input
DATAFRAMES_TO_MERGE = [
    r"C:\Users\totos\Desktop\11 - arXiv_pcfs_dataframe_identified_limits_merged_cfs_and_recurrences\pcfs_0-154047.pkl",
    r"C:\Users\totos\Desktop\12 - manual_pcfs\manual_pcfs_from_29.10.24.pkl",
    r"C:\Users\totos\Desktop\12 - cmf_pcfs\cmf_pcfs-('pi_cmf', 'symmetric_pi_cmf', '2F1')-max_i=8-generate_folds=True.pkl",
]

# output
SAVE_FILE = r'pcfs_28.12.24.pkl'

# defaults
SAVE_DIR = r"C:\Users\totos\Desktop\13 - merge_dataframes_and_sources"
SAVE_PATH = SAVE_DIR + '\\' + SAVE_FILE




def normalize_a_b(sympy_exp):
    return str(sp.expand(sympy_exp))


def merge_sources(df):
    # Add stringified columns for grouping
    df['a_str'] = df['a'].apply(normalize_a_b)
    df['b_str'] = df['b'].apply(normalize_a_b)

    # Initialize a list to store results
    results = []

    # Group by the stringified (a, b) pairs
    for (a_str, b_str), group in df.groupby(['a_str', 'b_str']):
        # Retrieve the original a and b from the first row of the group
        a = group['a'].iloc[0]
        b = group['b'].iloc[0]

        # Collect unique limits, excluding None
        unique_limits = list({limit for limit in group['limit'] if limit is not None})

        # Gather sources as dictionaries
        source_types = group['source_type'].unique()
        sources = group[['origin_formula_type', 'source_type', 'source', 'metadata', 'limit']].to_dict(orient='records')

        # Append results
        results.append({
            'a': a,
            'b': b,
            'limit': None if (len(unique_limits) == 0 or len(unique_limits) > 1) else unique_limits[0],
            'source_types': source_types,
            'limit_candidates': unique_limits,
            'sources': sources
        })

    # Convert the results into a new DataFrame
    processed_df = pd.DataFrame(results)

    # Clean up the temporary string columns
    df.drop(columns=['a_str', 'b_str'], inplace=True)
    return processed_df


def add_row_to_processed(processed_df, new_row):
    """
    Adds a new row from the original DataFrame to the processed DataFrame.

    Parameters:
        processed_df (pd.DataFrame): The processed DataFrame with unique (a, b) pairs.
        new_row (pd.Series): A row from the original DataFrame to add.

    Returns:
        pd.DataFrame: Updated processed DataFrame.
    """
    # Extract (a, b) pair from the new row
    a, b = new_row['a'], new_row['b']
    
    # Check if the pair already exists in the processed DataFrame
    existing_row = processed_df[(processed_df['a'].apply(normalize_a_b) == normalize_a_b(a)) & 
                                (processed_df['b'].apply(normalize_a_b) == normalize_a_b(b))]
    
    if not existing_row.empty:
        # Update existing row
        idx = existing_row.index[0]
        
        # Add unique limit to limit_candidates
        limit = new_row['limit']
        if limit is not None and limit not in processed_df.at[idx, 'limit_candidates']:
            processed_df.at[idx, 'limit_candidates'].append(limit)
        
        # Append new source details to sources
        new_source = {
            'origin_formula_type': new_row['origin_formula_type'],
            'source_type': new_row['source_type'],
            'source': new_row['source'],
            'metadata': new_row['metadata'],
            'limit': new_row['limit']
        }
        processed_df.at[idx, 'sources'].append(new_source)
    else:
        # Add new row to the processed DataFrame
        new_entry = {
            'a': a,
            'b': b,
            'limit': new_row['limit'],
            'source_types': [new_row['source_type']],
            'limit_candidates': [new_row['limit']] if new_row['limit'] is not None else [],
            'sources': [{
                'limit': new_row['limit'],
                'origin_formula_type': new_row['origin_formula_type'],
                'source_type': new_row['source_type'],
                'source': new_row['source'],
                'metadata': new_row['metadata']
            }]
        }
        processed_df = pd.concat([processed_df, pd.DataFrame([new_entry])], ignore_index=True)
    
    return processed_df


if __name__ == "__main__":
    # Load the dataframes
    dataframes = [pd.read_pickle(file) for file in DATAFRAMES_TO_MERGE]

    # Merge the dataframes
    merged_df = pd.concat(dataframes, ignore_index=True)

    # Process the merged dataframe
    processed_df = merge_sources(merged_df)

    # Save the processed dataframe
    processed_df.to_pickle(SAVE_PATH)
    print("Merged and processed data saved successfully.")
