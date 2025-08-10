import pandas as pd
import os
import sys

def merge_csv_in_subfolders(input_root, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    # Walk recursively through input_root
    for root, dirs, files in os.walk(input_root):
        csv_files = [f for f in files if f.endswith('.csv')]
        if not csv_files:
            continue 

        csv_paths = [os.path.join(root, f) for f in sorted(csv_files)]
        print(f"Found {len(csv_paths)} CSV files in folder: {root}")
        df_list = [pd.read_csv(f) for f in csv_paths]
        merged_df = pd.concat(df_list, ignore_index=True)
        timestamp_cols = [col for col in merged_df.columns if 'timestamp' in col.lower()]
        if timestamp_cols:
            merged_df = merged_df.sort_values(by=timestamp_cols[0])

        rel_path = os.path.relpath(root, input_root)
        filename = rel_path.replace(os.sep, '_') + "_combined.csv"
        output_path = os.path.join(output_folder, filename)

        # Save merged CSV
        merged_df.to_csv(output_path, index=False)
        print(f"Saved merged CSV: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python merge_nested_csvs.py <input_root_folder> <output_folder>")
        sys.exit(1)

    input_root = sys.argv[1]
    output_folder = sys.argv[2]
    merge_csv_in_subfolders(input_root, output_folder)
