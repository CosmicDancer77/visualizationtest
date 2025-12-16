import pandas as pd
import requests
from io import StringIO
import time
from datetime import datetime
import base64

# --- Configuration ---
# Replace with the actual raw URLs you copied
CSV_URL_1 = "https://raw.githubusercontent.com/mauforonda/dolares/refs/heads/main/buy_extra.csv"
CSV_URL_2 = "https://raw.githubusercontent.com/mauforonda/dolares/refs/heads/main/sell_extra.csv"

def upload_to_github(file_path, content, commit_message):
    """
    Commits a file update to the specified GitHub repository.
    """
    repo_url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/contents/{file_path}"
    headers = {
        "Authorization": f"token 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",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # 1. Check if the file already exists (to get its SHA)
    try:
        response = requests.get(repo_url, headers=headers)
        response.raise_for_status()
        existing_data = response.json()
        sha = existing_data.get('sha')
    except requests.exceptions.RequestException:
        # File doesn't exist, proceed without SHA
        sha = None

    # 2. Base64 encode the new content
    encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')

    # 3. Create the payload for the API request
    payload = {
        "message": commit_message,
        "content": encoded_content,
        "branch": GITHUB_BRANCH
    }
    # Include SHA only if updating an existing file
    if sha:
        payload['sha'] = sha

    # 4. Make the PUT request to create/update the file
    try:
        put_response = requests.put(repo_url, headers=headers, json=payload)
        put_response.raise_for_status()
        print(f"✅ Successfully committed {file_path} to GitHub.")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Error committing {file_path} to GitHub: {e}")
        if put_response is not None:
             print(f"Response error details: {put_response.json()}")
        return False

def fetch_and_process_csv(url, file_name, github_file_path):
    """
    Fetches CSV data, returns a DataFrame, and commits the updated CSV
    content directly to GitHub.
    """
    try:
        # ... (Steps 1 & 2 remain the same: fetch and read CSV into df) ...
        response = requests.get(url, timeout=10)
        response.raise_for_status() 

        data = StringIO(response.text)
        df = pd.read_csv(data)

        # NEW: Get the CSV content as a string
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        updated_csv_content = csv_buffer.getvalue()

        # NEW: Upload the content to GitHub
        commit_message = f"Update {github_file_path} with latest data"
        upload_to_github(github_file_path, updated_csv_content, commit_message)
        
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Successfully processed data for {file_name}.")
        return df

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {file_name}: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred for {file_name}: {e}")
        return None

def main_update_script():
    """Main function to run the update and upload process."""
    print("--- Starting Scheduled Update ---")
    
    # NEW: Pass the target GitHub file path as the third argument
    # If the file is in the root, the path is just the filename.
    df1 = fetch_and_process_csv(CSV_URL_1, "File 1 (buy_extra)", "buy_extra.csv")
    if df1 is not None:
        print(f"File 1 shape: {df1.shape}")

    df2 = fetch_and_process_csv(CSV_URL_2, "File 2 (sell_extra)", "sell_extra.csv")
    if df2 is not None:
        print(f"File 2 shape: {df2.shape}")
        
    print("--- Scheduled Update Complete ---")

if __name__ == "__main__":
    main_update_script()
