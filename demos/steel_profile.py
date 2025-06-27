from morb_fetch import get_config, print_config, Database, Example

# Print configuration details of the package
config = get_config()
print_config()

# Database
database = Database(config)

# Lookup example ID and fetch data from cache/server
example = Example("steelProfile_n1357m7q6", database=database)
example.retrieve()
