import requests
import pandas as pd
import json

# Load the country alpha-2 codes from the JSON file
with open("country_alpha2_codes.json", "r") as json_file:
    country_alpha2_codes = json.load(json_file)

# Define the API endpoint URL with a placeholder for the country code
url = "https://api.globalplasticwatch.org/countries/{}/sites"

# Provide the API key as a parameter
params = {"apikey": "ksjdhfbo8e745g834gkajsdblkasjhbd2983874"}

# Initialize an empty list to hold all the country data
all_country_data = []

# Loop through the dictionary to fetch data for each country
for country, code in country_alpha2_codes.items():
    # Format the URL with the country code
    formatted_url = url.format(code)

    # Send a GET request to the API endpoint
    response = requests.get(formatted_url, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Flatten the nested JSON structure
        flattened_data = []
        for feature in data["features"]:
            properties = feature["properties"]
            geometry = feature["geometry"]
            properties.update(geometry)
            flattened_data.append(properties)

        # Extend the all_country_data list with the flattened data
        all_country_data.extend(flattened_data)

        print(f"Data for {country} fetched successfully")
    else:
        # Print an error message if the request was not successful
        print(f"Failed to fetch data for {country} from the API")

# Convert the list of dictionaries into a DataFrame
df = pd.DataFrame(all_country_data)

# Define the file path where you want to save the CSV file
file_path = "data/country_sites.csv"

# Save the DataFrame to a CSV file
df.to_csv(file_path, index=False)

print(f"Country sites data saved successfully to: {file_path}")
