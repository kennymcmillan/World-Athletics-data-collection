

from setup import *

# Introspection query to get the schema
introspection_query = """
{
  __schema {
    types {
      name
      fields {
        name
        type {
          name
        }
      }
    }
  }
}
"""

api = API(query=introspection_query)
schema_data = api.fetch_data()

# Save the schema data to a file for analysis
with open('schema.json', 'w') as f:
    json.dump(schema_data, f, indent=2)

print("Schema data saved to schema.json")