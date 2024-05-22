import requests
import pandas as pd
import json

# Load the country alpha-2 codes from the JSON file
with open("country_alpha2_codes.json", "r") as json_file:
    country_alpha2_codes = json.load(json_file)

# Define the API endpoint URL with a placeholder for the country code
url = "https://api.globalplasticwatch.org/countries/{}/stats"

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
        flattened_data = {
            "country": country,
            "totalSites": data["totalSites"],
            "name": data["name"],
            "surface_total": data["surface"]["total"],
            "surface_oneKM": data["surface"]["oneKM"],
            "surface_tenKM": data["surface"]["tenKM"],
            "water_m250": data["water"]["m250"],
            "water_m500": data["water"]["m500"],
            "water_oneKM": data["water"]["oneKM"],
            "people_tenKM": data["people"]["tenKM"],
            "people_oneKM": data["people"]["oneKM"],
            "people_fiveKM": data["people"]["fiveKM"],
            "indexYear": data["index"]["indexYear"],
            "kgPerCaptia": data["index"]["kgPerCaptia"],
            "rank": data["index"]["rank"],
        }

        # Extract top producers information with error handling
        top_producers = data["index"]["topProducers"]
        top_producer_keys = list(top_producers.keys())
        top_producer_values = list(top_producers.values())

        # Assign default values if 'topProducers' doesn't have enough entries
        for i in range(1, 6):
            key = f"topProducer_{i}"
            value_key = f"topProducer_{i}_value"
            flattened_data[key] = (
                top_producer_keys[i - 1] if i <= len(top_producer_keys) else None
            )
            flattened_data[value_key] = (
                top_producer_values[i - 1] if i <= len(top_producer_values) else None
            )

        # Append the flattened data to the list
        all_country_data.append(flattened_data)

        print(f"Data for {country} fetched successfully")
    else:
        # Print an error message if the request was not successful
        print(f"Failed to fetch data for {country} from the API")

# Convert the list of dictionaries into a DataFrame
country_info = pd.DataFrame(all_country_data)

# Define the file path where you want to save the CSV file
file_path = "data/country_info.csv"

# Save the DataFrame to a CSV file
country_info.to_csv(file_path, index=False)

print(f"country_info saved successfully to: {file_path}")
