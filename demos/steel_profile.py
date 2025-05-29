from morwiki import print_config, Example

# Print configuration details of the package
print_config()

# Lookup example ID and fetch data from cache/server
example = Example('steelProfile_n1357m7q6')
example.retrieve()
