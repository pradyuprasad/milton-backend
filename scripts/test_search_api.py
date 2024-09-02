import requests


def search_query(query: str):
    response = requests.post(
        "http://localhost:10000/search", json={"user_query": query}
    )

    return response.json()


answer = search_query("What is the inflation rate in the US?")
print(answer)
