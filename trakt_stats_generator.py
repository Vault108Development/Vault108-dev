import json
import requests
import os

def split_time_string(minutes):
    """
    Splits a time string into two parts for multi-line display in SVG,
    showing total days and total hours without rounding.
    """
    total_days = minutes // 1440
    
    # Return days only
    return f"{total_days:,} days"

def generate_svg_content(movies_watched, shows_watched, episodes_watched, total_minutes, shows_minutes, movies_minutes):
    """
    Generates and saves the SVG image based on the provided statistics.
    """
    # Split the time strings for SVG display
    total_time_line = split_time_string(total_minutes)
    shows_time_line = split_time_string(shows_minutes)
    movies_time_line = split_time_string(movies_minutes)
    
    # Define the SVG content as a string
    svg_content = f"""
    <svg width="600" height="400" viewBox="0 0 600 400" xmlns="http://www.w3.org/2000/svg">
        <rect width="100%" height="100%" fill="#f9fafb" rx="15" ry="15"/>

        <text x="30" y="50" font-family="sans-serif" font-size="28" font-weight="bold" fill="#1f2937">Trakt.tv Statistics</text>
        

        <g transform="translate(30, 150)">
            <text y="0" font-family="sans-serif" font-size="20" fill="#374151">Shows Watched:</text>
            <text y="0" x="250" font-family="sans-serif" font-size="20" font-weight="bold" fill="#4b5563">{shows_watched}</text>
        </g>
        
        <g transform="translate(30, 190)">
            <text y="0" font-family="sans-serif" font-size="20" fill="#374151">Episodes Watched:</text>
            <text y="0" x="250" font-family="sans-serif" font-size="20" font-weight="bold" fill="#4b5563">{episodes_watched}</text>
        </g>

        <g transform="translate(30, 230)">
            <text y="0" font-family="sans-serif" font-size="20" fill="#374151">Movies Watched:</text>
            <text y="0" x="250" font-family="sans-serif" font-size="20" font-weight="bold" fill="#4b5563">{movies_watched}</text>
        </g>

        <g transform="translate(30, 270)">
            <text y="0" font-family="sans-serif" font-size="20" fill="#374151">Total Time Watched:</text>
            <text x="250" y="0" font-family="sans-serif" font-size="20" font-weight="bold" fill="#4b5563">
                {total_time_line}
            </text>
        </g>

        <g transform="translate(30, 310)">
            <text y="0" font-family="sans-serif" font-size="20" fill="#374151">Time on Shows:</text>
            <text x="250" y="0" font-family="sans-serif" font-size="20" font-weight="bold" fill="#4b5563">
                {shows_time_line}
            </text>
        </g>

        <g transform="translate(30, 350)">
            <text y="0" font-family="sans-serif" font-size="20" fill="#374151">Time on Movies:</text>
            <text x="250" y="0" font-family="sans-serif" font-size="20" font-weight="bold" fill="#4b5563">
                {movies_time_line}
            </text>
        </g>
    </svg>
    """

    # Define the output file name
    output_file_name = "assets/trakt_stats.svg"
    
    # Save the SVG string to a file
    with open(output_file_name, "w") as f:
        f.write(svg_content)
    
    print(f"Successfully generated and saved the SVG to {output_file_name}")

def generate_stats_svg():
    """
    Generates an SVG image of Trakt.tv user statistics by fetching data from the API.
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

        movies_watched = data["movies"]["watched"]
        shows_watched = data["shows"]["watched"]
        episodes_watched = data["episodes"]["watched"]
        movies_minutes = data["movies"]["minutes"]
        episodes_minutes = data["episodes"]["minutes"]
        total_minutes = movies_minutes + episodes_minutes

        # Call the new function to generate the SVG
        generate_svg_content(movies_watched, shows_watched, episodes_watched, total_minutes, episodes_minutes, movies_minutes)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the API request: {e}")
    except json.JSONDecodeError:
        print("Error: Failed to parse JSON data from the API response.")
    except KeyError as e:
        print(f"Error: Missing key in data: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Run the function to generate the SVG
if __name__ == "__main__":
    generate_stats_svg()
