import pandas as pd
import requests as re
import json
import sys
import warnings
import os

currentwd = os.getcwd()
api_path = os.path.join(currentwd, 'api.json')

from pandas.errors import SettingWithCopyWarning
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)
warnings.simplefilter(action="ignore", category=FutureWarning)

class API:
    def __init__(self, query, variables=None, config_file='api_path'):
        with open(config_file) as f:
            data = json.load(f)
        self.apiEndPoint = data['apiEndPoint']
        self.apiKey = data['apiKey']
        self.headers = {
            'Accept': '*/*',
            'Content-Type': 'application/json',
            'User-Agent': 'PostmanRuntime/7.29.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'x-api-key': self.apiKey
        }
        self.query = query
        self.variables = variables

    def fetch_data(self):
        try:
            response = re.post(
                url=self.apiEndPoint,
                headers=self.headers,
                json={
                    "query": self.query,
                    "variables": self.variables
                }
            )
            response.raise_for_status()
            return response.json()
        except re.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")
        sys.exit("Failed to fetch data from the API!")

# Define the GraphQL query
query = '''
query {
  getAllCompetitions {
    pageNextEvent {
      id
      name
      description
      urlSlug
      nextEventStartDate
    }
    allEvents {
      id
      name
      description
      urlSlug
      nextEventStartDate
      lastEvent {
        id
        name
        startDate
        endDate
      }
    }
  }
}
'''

# Create an instance of the API class
api = API(query)

# Fetch data
data = api.fetch_data()

# Print the fetched data
print(json.dumps(data, indent=2))
