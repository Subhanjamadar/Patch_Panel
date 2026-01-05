# model_cache.py

# This dictionary maps switch IPs to their corresponding models
ip_model_map = {
    # Add your switch IP to model mappings here
    # Example:
    # "10.22.74.11": "Aruba 6410",
    # "10.22.74.12": "ProCurve 5412zl",
}

def update_models_from_excel(file_path):
    """
    Update the ip_model_map from an Excel file
    Expected Excel format: Columns "EOR IP Address" and "Model Name"
    """
    try:
        import pandas as pd
        df = pd.read_excel(file_path)
        for _, row in df.iterrows():
            ip = str(row["EOR IP Address"]).strip()
            model = str(row["Model Name"]).strip()
            if ip and model:  # Only add non-empty entries
                ip_model_map[ip] = model
        print(f"Successfully loaded {len(ip_model_map)} switch models from {file_path}")
        return True
    except Exception as e:
        print(f"Error loading switch models from Excel: {str(e)}")
        return False

# Load models from Excel if the file exists
try:
    update_models_from_excel("EOR Switch Details - Current.xlsx")
except Exception as e:
    print(f"Could not load switch models from Excel: {str(e)}")

# Add any hardcoded models as fallback
hardcoded_models = {
    "10.22.74.11": "Aruba 6410",
    "10.22.74.12": "ProCurve 5412zl",
    "10.22.74.13": "Aruba 6410",
    "10.22.74.14": "Aruba 6410",
    "10.22.74.15": "Aruba 6410",
    "10.22.74.16": "Aruba 6410",
    "10.22.74.17": "Aruba 6410",
    "10.22.74.18": "Aruba 6410",
    "10.22.74.19": "Aruba 6410",
    "10.22.74.20": "Aruba 6410",
    "10.22.74.22": "Aruba 3810M 48G",
    "10.22.74.23": "Aruba 6410",
    "10.22.74.24": "Aruba 6410",
    "10.22.74.25": "Aruba 6410",
    "10.22.74.26": "Aruba 6410",
    "10.22.74.27": "HP 2510G-48",
    "10.22.74.29": "Aruba 5400R zl2",
    "10.22.74.30": "Aruba 5400R zl2",
    "10.22.75.11": "H3C",
    "10.22.75.12": "Aruba 5400R zl2",
    "10.22.75.13": "Aruba 6410",
    "10.22.75.14": "H3C",
    "10.22.75.15": "H3C",
    "10.22.75.16": "Aruba 6410",
    "10.22.75.17": "Aruba 6410",
    "10.22.75.18": "Aruba 6410",
    "10.22.75.19": "Aruba 6410",
    "10.22.75.20": "Aruba 6410",
    "10.22.75.22": "Aruba 6410",
    "10.22.75.23": "Aruba 6410",
    "10.22.75.24": "Aruba 6410",
    "10.22.75.25": "Aruba 6410",
    "10.22.75.26": "Aruba 6410",
    "10.22.76.11": "HP 2910",
    "10.22.76.12": "HPE 5900F-48G",
    "10.22.76.13": "Aruba 6410",
    "10.22.76.14": "Aruba 6410",
    "10.22.76.15": "Aruba 6410",
    "10.22.76.16": "Aruba 5400R zl2",
    "10.22.76.19": "H3C",
    "10.22.76.20": "Aruba 6410",
    "10.22.76.21": "Aruba 6410",
    "10.22.76.22": "Aruba 6410",
    "10.22.76.23": "Aruba 6410",
    "10.22.76.24": "Aruba 5400 zl2",
    "10.22.76.25": "Aruba 6410",
    "10.22.76.26": "Aruba 6410",
    "10.22.77.11": "Aruba 6410",
    "10.22.77.12": "Aruba 6410",
    "10.22.77.13": "Aruba 6410",
    "10.22.77.14": "Aruba 6410",
    "10.22.77.15": "Aruba 6410",
    "10.22.77.16": "Aruba 6410",
    "10.22.77.17": "Aruba 6410",
    "10.22.77.18": "Aruba 6410",
    "10.22.77.19": "H3C",
    "10.22.77.20": "Aruba 6410",
    "10.22.77.21": "Aruba 6410",
    "10.22.77.22": "Aruba 5400 zl2",
    "10.22.77.23": "Aruba 6410",
    "10.22.77.24": "Aruba 6410",
    "10.22.77.25": "Aruba 6410",
    "10.22.77.26": "Aruba 6410",
    "10.22.77.27": "Aruba 6410",
    "10.22.77.28": "Aruba 5400 zl2",
    "10.22.78.11": "Aruba 6410",
    "10.22.78.12": "Aruba 6410",
    "10.22.78.13": "Aruba 6410",
    "10.22.78.14": "Aruba 6410",
    "10.22.78.15": "Aruba 6410",
    "10.22.78.16": "Aruba 5400 zl2",
    "10.22.78.9": "Aruba 8325",
    "10.22.78.10": "Aruba 8325",
    "10.22.78.19": "Aruba 6410",
    "10.22.78.20": "Aruba 5400R zl2",
    "10.22.78.21": "Aruba 6410",
    "10.22.78.22": "Aruba 5400R zl2",
    "10.22.78.23": "Aruba 6410",
    "10.22.78.24": "Aruba 5400R zl2",
    "10.22.78.25": "H3C",
    "10.22.78.26": "Aruba 6410",
    "10.22.78.28": "Aruba 6410",
    "10.22.78.27": "Aruba 6410",
    "10.22.78.29": "Aruba 2930F 48G"

}
ip_model_map.update(hardcoded_models)