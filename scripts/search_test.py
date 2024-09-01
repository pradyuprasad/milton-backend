from src.milton_backend.search.search import SearchClient


client = SearchClient()

client.search("GDP", verbose=True)
