import pandas as pd
import requests as re
import json
import sys
import warnings

from pandas.errors import SettingWithCopyWarning
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)
warnings.simplefilter(action="ignore", category=FutureWarning)

class API:
    def __init__(self, query, variables=None):
        self.apiEndPoint = "https://u6ao74frprd43gdloanuo7m4xy.appsync-api.eu-west-1.amazonaws.com/graphql"
        self.apiKey = "da2-cdks2epcureyzjhk5jif4b2hxa"
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

def process_data(api_response):
    try:
        # Print the entire response to understand its structure
        print("API Response:", json.dumps(api_response, indent=2))

        # Extract the data based on the actual response structure
        if 'data' in api_response and 'getCompetitors' in api_response['data']:
            data = api_response['data']['getCompetitors']
            df = pd.json_normalize(data)

            # Filter by country code QAT (Qatar)
            df_filtered = df[df['countryCode'] == 'QAT']
            return df_filtered
        else:
            sys.exit("Unexpected response structure!")
    except KeyError as e:
        sys.exit(f"KeyError: {e} - Could not find the expected key in the API response!")
    except Exception as e:
        sys.exit(f"An error occurred during data processing: {e}")

if __name__ == "__main__":
    query = """
    query getCompetitors($countryCode: String!) {
      getCompetitors(countryCode: $countryCode) {
        competitorId
        firstName
        lastName
        birthDate
        birthPlace
        countryName
        countryCode
        sexName
        teamName
        fullBio
      }
    }
    """
    variables = {"countryCode": "QAT"}

    api = API(query=query, variables=variables)
    response_data = api.fetch_data()

    df = process_data(response_data)
    print(df)
