import pandas as pd
import requests as re
import json
import sys
import warnings

from pandas.errors import SettingWithCopyWarning
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)
warnings.simplefilter(action="ignore", category=FutureWarning)

class API:
    def __init__(self, query, variables=None, config_file='api.json'):
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

def searchCompetitor(query=None, gender=None, disciplineCode=None, environment=None, countryCode=None):
    # Assuming config.searchCompetitorQuery contains the actual GraphQL query
    queryBody = """
    query searchCompetitor($query: String, $gender: String, $disciplineCode: String, $environment: String, $countryCode: String) {
      searchCompetitors(query: $query, gender: $gender, disciplineCode: $disciplineCode, environment: $environment, countryCode: $countryCode) {
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
    queryVariables = {
        "query": query,
        "gender": gender,
        "disciplineCode": disciplineCode,
        "environment": environment,
        "countryCode": countryCode,
    }
    json_data = API(queryBody, queryVariables).fetch_data()
    if json_data['data']['searchCompetitors'] is None:
        print("Search not found for", query, countryCode, ".")
        return pd.DataFrame()  # Return an empty DataFrame if no data found
    df = pd.DataFrame.from_dict(json_data['data']['searchCompetitors'])
    return df

if __name__ == "__main__":
    # Search for competitors from Qatar (QAT)
    df_qatar_competitors = searchCompetitor(countryCode="QAT")
    print(df_qatar_competitors)
