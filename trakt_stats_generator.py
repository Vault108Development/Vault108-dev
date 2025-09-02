import json
import requests
import os

def generate_stats_json():
    """
    Generates a JSON file of Trakt.tv user statistics by fetching data from the API,
    adds new 'hours' and 'days' keys to the data, and saves the full response.
    """
    url = "https://api.trakt.tv/users/vault108/stats"
    trakt_api_key = os.environ.get('TRAKT_API_KEY')

    if not trakt_api_key:
        print("Error: The TRAKT_API_KEY environment variable is not set.")
        return

    payload = {}
    headers = {
      'Content-Type': 'application/json',
      'trakt-api-version': '2',
      'trakt-api-key': trakt_api_key
    }

    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        response.raise_for_status()  # This will raise an exception for HTTP errors
        
        data = json.loads(response.text)
        
        # Calculate and add 'hours' and 'days' keys to the JSON data
        if 'movies' in data and 'minutes' in data['movies']:
            data['movies']['hours'] = round(data['movies']['minutes'] / 60, 2)
            data['movies']['days'] = round(data['movies']['minutes'] / 1440, 2)
        
        if 'episodes' in data and 'minutes' in data['episodes']:
            data['episodes']['hours'] = round(data['episodes']['minutes'] / 60, 2)
            data['episodes']['days'] = round(data['episodes']['minutes'] / 1440, 2)
            
        if 'shows' in data and 'minutes' in data['shows']:
            data['shows']['hours'] = round(data['shows']['minutes'] / 60, 2)
            data['shows']['days'] = round(data['shows']['minutes'] / 1440, 2)
        
        # Log the full JSON data to the console
        print("Generated JSON data:")
        print(json.dumps(data, indent=4))

        # Define the output file name
        output_file_name = "assets/trakt_stats.json"
        
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
