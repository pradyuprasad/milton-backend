from src.milton_backend.search.search import SearchClient
from src.milton_backend.common.models import ClassifiedSeries


client = SearchClient()

ans: ClassifiedSeries = client.search("GDP", verbose=False)

print(" the relevant series are: ", ans.relevant)
print("the not revelant series are: ", ans.notRelevant)
