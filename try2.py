

import requests

# Define the GraphQL endpoint URL and API key
url = 'https://u6ao74frprd43gdloanuo7m4xy.appsync-api.eu-west-1.amazonaws.com/graphql'
api_key = 'da2-cdks2epcureyzjhk5jif4b2hxa'

# Define the GraphQL query
query = """
{
  getWorldRanking {
    id
    place
    worldPlace
    athlete
    athleteUrlSlug
    birthDate
    nationality
    rankingScore
    disciplines
    countryPlace
    previousId
    previousPlace
    previousRankingScore
  }
}
"""

# Define the headers
headers = {
    'Content-Type': 'application/json',
    'x-api-key': api_key
}

# Make the POST request to the GraphQL endpoint
response = requests.post(url, json={'query': query}, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    # Extract the data you're interested in
    rankings = data['data']['getWorldRanking']
    for ranking in rankings:
        print(f"ID: {ranking['id']}, Athlete: {ranking['athlete']}, Place: {ranking['place']}")
else:
    print(f"Failed to fetch data: {response.status_code}")
