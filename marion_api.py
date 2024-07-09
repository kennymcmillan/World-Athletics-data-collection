import requests
import pandas as pd

# Define the base URL for the API
base_url = "https://worldathletics.nimarion.de/"

# Define the endpoint for getting countries
endpoint = "/countries"

# Make the GET request
response = requests.get(base_url + endpoint)
countries_data = response.json()
df_countries = pd.DataFrame(countries_data)
print(df_countries)


endpoint = "/disciplines"
response = requests.get(base_url + endpoint)
countries_data = response.json()
df_disciplines= pd.DataFrame(countries_data)
print(df_disciplines)
