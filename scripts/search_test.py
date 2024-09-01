from . import SearchClient

client = SearchClient()
ans = client.find_relevant_series(query="What is the GDP of the USA", verbose=True)
