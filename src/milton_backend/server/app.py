from fastapi import FastAPI
from src.milton_backend.common.models import ClassifiedSeries
from src.milton_backend.search.search import SearchClient
from .models import QueryModel

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/search")
def search(query: QueryModel) -> ClassifiedSeries:
    client = SearchClient()
    return client.search(query.user_query)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=10000)
