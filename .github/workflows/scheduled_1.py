import pandas as pd
import requests
from io import StringIO
import time
from datetime import datetime

# --- Configuration ---
# Replace with the actual raw URLs you copied
CSV_URL_1 = "https://raw.githubusercontent.com/mauforonda/dolares/refs/heads/main/buy_extra.csv"
CSV_URL_2 = "https://raw.githubusercontent.com/mauforonda/dolares/refs/heads/main/sell_extra.csv"

def fetch_and_process_csv(url, file_name):
    """Fetches CSV data from a URL and returns a pandas DataFrame."""
    try:
        # 1. Fetch the data using requests
        response = requests.get(url, timeout=10)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

        # 2. Read the raw text content into a pandas DataFrame
        # StringIO treats the string content like a file
        data = StringIO(response.text)
        df = pd.read_csv(data)

        # Optional: Save the updated data to a local file for persistence
        df.to_csv(f"{file_name}_updated.csv", index=False)
        
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Successfully updated data for {file_name}.")
        return df

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {file_name}: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred for {file_name}: {e}")
        return None

def main_update_script():
    """Main function to run the update process for both files."""
    print("--- Starting Scheduled Update ---")
    
    # Fetch File 1
    df1 = fetch_and_process_csv(CSV_URL_1, "file1")
    if df1 is not None:
        print(f"File 1 shape: {df1.shape}")
        # Your custom processing/analysis logic for df1 goes here
        # Example: print(df1.head())

    # Fetch File 2
    df2 = fetch_and_process_csv(CSV_URL_2, "file2")
    if df2 is not None:
        print(f"File 2 shape: {df2.shape}")
        # Your custom processing/analysis logic for df2 goes here
        # Example: print(df2.describe())
    
    print("--- Scheduled Update Complete ---")

# If you run the script directly, it will perform one update
if __name__ == "__main__":
    main_update_script()