from typing import List, Set
from threading import Lock
from src.milton_backend.config.config import Config
import instructor
from groq import Groq
from openai import OpenAI
from src.milton_backend.common.models import Keywords, SeriesForSearch, ClassifiedSeries
from src.milton_backend.vector_db import ChromaDBClient


class SearchClient:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(SearchClient, cls).__new__(cls)
                    cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.config = Config()
        self.chroma_db_client = ChromaDBClient()
        self.groq_instructor_client = instructor.from_groq(Groq(api_key=self.config.get("GROQ_API_KEY")))
        self.openai_instructor_client = instructor.from_openai(OpenAI(api_key=self.config.get('OPENAI_API_KEY')))
    
    def __extract_keyword(self, user_query: str) -> Keywords:
        return self.openai_instructor_client.chat.completions.create(
            model="gpt-4o-mini",
            response_model=Keywords,
            messages=[
                {"role": "system", "content": """
        You are an expert in economic terminology and the FRED (Federal Reserve Economic Data) database. Your task is to convert user queries into the most appropriate search terms for the FRED database.
                """},
                {"role": "user", "content": f"""
        Convert the following query into search terms for the FRED database:
        "{user_query}"
        Follow these rules strictly:
        1. Provide only full terms as they would appear in the FRED database. For example, use "Gross Domestic Product" instead of "GDP".
        2. Expand all common economic acronyms to their full forms.
        3. Focus on specific economic indicators, measurements, or concepts.
        4. Provide at most 3 key terms, prioritizing specificity and relevance to the FRED database. 
        5. Do not include general words like "current", "rate" unless they are part of a specific economic term.
        6. If the query mentions a specific country, include the full country name as part of the relevant economic term(s).
        Respond with only the list of search terms, nothing else.
        7. Be strict in your question. Ensure that the geographic region and all other data match what the user asked
                """}
            ]
        )

    def __keyword_semantic_search(self, keywords: List[str], n_results: int = 5, verbose:bool = False) -> Set[SeriesForSearch]:
        chromaDB = ChromaDBClient()
        series_collection = chromaDB.get_or_create_collection("fred-economic-series")

        
        results = []

        
        #query = ' '.join(keywords)

        keyword_results = series_collection.query(query_texts=keywords, n_results=n_results)
        if verbose:
            print("the query is", keywords, "and the results are", keyword_results)
        results.append(keyword_results)


        series_set = set()
        
        for keyword_results in results:
            for i in range(len(keyword_results['ids'][0])):
                series = SeriesForSearch(
                    fred_id=keyword_results['ids'][0][i],
                    title=keyword_results['metadatas'][0][i]['title'],
                    units=keyword_results['metadatas'][0][i]['units'],
                    popularity=keyword_results['metadatas'][0][i]['popularity'],
                    relevance_lower_better=keyword_results['distances'][0][i]
                )
                series_set.add(series)
        
        return series_set

    def __rank_relevant_outputs(self, series_list:List[SeriesForSearch], query:str) -> ClassifiedSeries:
        
        return self.openai_instructor_client.chat.completions.create(response_model=ClassifiedSeries, messages=[
            {"role": "system", "content": "You will be given a number of economic series from the user. Your job is to mark them as relevant or irrelevant for a given query and output it in the given format"}, {
                "role": "user", "content":f"The user's query is {query}. The possible datasets are {series_list}"
            }
        ], model="gpt-4o-mini")
    
    def search(self, user_query: str, verbose:bool = False) -> ClassifiedSeries:
        ans: Keywords = self.__extract_keyword(user_query)
        if verbose:
            print("keywords are", (ans.keyword_list))
        
        raw_series:Set[SeriesForSearch] = self.__keyword_semantic_search(keywords=ans.keyword_list, n_results=5)
        if verbose:
            print("raw series are", raw_series)
        ranked_series: ClassifiedSeries = self.__rank_relevant_outputs(raw_series, user_query)
        if verbose:
            print("ranked series are", ranked_series)
        return ranked_series

