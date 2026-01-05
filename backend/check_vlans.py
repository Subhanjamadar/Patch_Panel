import pandas as pd

try:
    # Read the Excel file
    df = pd.read_excel("VLANS.xlsx")
    
    # Display basic information about the file
    print("File read successfully!")
    print("\nFirst few rows of the file:")
    print(df.head())
    
    # Display column names
    print("\nColumn names:", df.columns.tolist())
    
    # Check if 'Floor Name' column exists
    if 'Floor Name' in df.columns:
        print("\nUnique floor names in 'Floor Name' column:")
        print(df['Floor Name'].dropna().unique())
    else:
        print("\n'Floor Name' column not found in the Excel file.")
        print("Available columns:", df.columns.tolist())
        
    # Check if 'VLAN ID' column exists
    if 'VLAN ID' in df.columns:
        print("\nSample VLAN IDs:")
        print(df['VLAN ID'].dropna().head().tolist())
    else:
        print("\n'VLAN ID' column not found in the Excel file.")
        
except Exception as e:
    print(f"Error reading VLANS.xlsx: {str(e)}")
