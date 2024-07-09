
import worldathletics
import requests

# Initialize the API client
api_key = 'da2-cdks2epcureyzjhk5jif4b2hxa'
api_url = 'https://u6ao74frprd43gdloanuo7m4xy.appsync-api.eu-west-1.amazonaws.com/graphql'


# Function to fetch all athletes
def fetch_all_athletes():
    all_athletes = []
    next_token = None
    limit = 100  # Number of athletes per request

    while True:
        # Define the GraphQL query with pagination
        query = '''
        query SearchAthletes($limit: Int!, $nextToken: String) {
          searchAthletes(limit: $limit, nextToken: $nextToken) {
            items {
              id
              firstName
              lastName
            }
            nextToken
          }
        }
        '''
        
        variables = {"limit": limit, "nextToken": next_token}
        headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json"
        }
        
        response = requests.post(api_url, json={'query': query, 'variables': variables}, headers=headers)
        if response.status_code == 200:
            result = response.json()
            try:
                athletes = result['data']['searchAthletes']['items']
                all_athletes.extend(athletes)
                next_token = result['data']['searchAthletes']['nextToken']
                if not next_token:
                    break
            except KeyError as e:
                print(f"KeyError: {e} in response: {result}")
                break
        else:
            print(f"Error: {response.status_code}, {response.text}")
            break
    
    return all_athletes

# Fetch all athletes
all_athletes = fetch_all_athletes()
print(f"Total Athletes Retrieved: {len(all_athletes)}")
for athlete in all_athletes:
    print(f"{athlete['firstName']} {athlete['lastName']}")