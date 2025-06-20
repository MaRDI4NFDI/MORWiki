from morwiki import print_config, Example

# Print configuration details of the package
print_config()

# Lookup example ID and fetch data from cache/server
example = Example("plateTVA_n201900m1q1")
example.retrieve()
