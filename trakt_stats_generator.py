import json
import requests
import os
import datetime

def generate_stats_json():
    """
    Generates a JSON file of Trakt.tv user statistics by fetching data from the API,
    adds new 'hours' and 'days' keys to the data, and saves the full response.
    """
    url = "https://api.trakt.tv/users/vault108/stats"
    trakt_api_key = os.environ.get('TRAKT_API_KEY')

    if not trakt_api_key:
        print("Error: The TRAKT_API_KEY environment variable is not set. Please set it before running the script.")
        return

    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'trakt-api-version': '2',
        'trakt-api-key': trakt_api_key
    }

    try:
        print("Attempting to fetch data from Trakt.tv API...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # This will raise an exception for HTTP errors
        
        data = response.json()
        
        # Calculate and add 'hours' and 'days' keys to the JSON data, rounding to the nearest whole number
        if 'movies' in data and 'minutes' in data['movies']:
            data['movies']['hours'] = round(data['movies']['minutes'] / 60)
            data['movies']['days'] = round(data['movies']['minutes'] / 1440)
        
        if 'episodes' in data and 'minutes' in data['episodes']:
            data['episodes']['hours'] = round(data['episodes']['minutes'] / 60)
            data['episodes']['days'] = round(data['episodes']['minutes'] / 1440)
            
        if 'shows' in data and 'minutes' in data['shows']:
            data['shows']['hours'] = round(data['shows']['minutes'] / 60)
            data['shows']['days'] = round(data['shows']['minutes'] / 1440)

        # Add a timestamp to force a file change
        data['last_updated'] = datetime.datetime.now().isoformat()
        
        # Log the full JSON data to the console
        print("Generated JSON data:")
        print(json.dumps(data, indent=4))

        # --- FIX: Use a robust, absolute path for the output file ---
        # Get the directory where the script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Construct the full path to the output file using os.path.join for cross-platform compatibility
        output_dir = os.path.join(script_dir, "assets")
        output_file_name = os.path.join(output_dir, "trakt_stats.json")
        
        # Ensure the assets directory exists
        os.makedirs(output_dir, exist_ok=True)
        print(f"Directory '{output_dir}' confirmed to exist or was created.")
        
        print(f"Attempting to save JSON to file: {output_file_name}")
        
        # Save the full JSON response to a file
        with open(output_file_name, "w") as f:
            json.dump(data, f, indent=4)
        
        print(f"Successfully generated and saved the full JSON to {output_file_name}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the API request: {e}")
    except json.JSONDecodeError:
        print("Error: Failed to parse JSON data from the API response.")
    except KeyError as e:
        print(f"Error: Missing key in data: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Run the function to generate the JSON
if __name__ == "__main__":
    generate_stats_json()
