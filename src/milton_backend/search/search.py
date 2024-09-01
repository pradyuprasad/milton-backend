from typing import List, Set
from threading import Lock
from src.milton_backend.vector_db import ChromaDBClient
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
    
    def extract_keyword(self, user_query: str) -> Keywords:
        """
        Extract the most relevant search terms from a user query for the FRED (Federal Reserve Economic Data) database.

        Parameters:
        user_query (str): The user query to be converted into search terms.

        Returns:
        Keywords: The most relevant search terms for the FRED database, as a list of strings.

        Rules that are strictly followed when generating the search terms:
        1. Provide only full terms as they would appear in the FRED database. For example, use "Gross Domestic Product" instead of "GDP".
        2. Expand all common economic acronyms to their full forms.
        3. Focus on specific economic indicators, measurements, or concepts.
        4. Provide at most 3 key terms, prioritizing specificity and relevance to the FRED database. 
        5. Do not include general words like "current", "rate" unless they are part of a specific economic term.
        6. If the query mentions a specific country, include the full country name as part of the relevant economic term(s).
        7. Be strict in your question. Ensure that the geographic region and all other data match what the user asked
        """
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

def keyword_semantic_search(keywords: List[str], n_results: int = 5, verbose:bool = False) -> Set[SeriesForSearch]:
    chromaDB = ChromaDBClient()
    series_collection = chromaDB.get_or_create_collection("fred-economic-series")

    
    results = []
    ''' # TODO: Decide if this is needed or not
    for keyword in keywords:
        # Assuming collection.query is defined and functional
        keyword_results = collection.query(
            query_texts=[keyword],
            n_results=n_results
        )
        if verbose:
            print("the keyword is", keyword, "and the results are", keyword_results)
        results.append(keyword_results)
    '''
    
    query = ' '.join(keywords)

    keyword_results = series_collection.query(query_texts=[query], n_results=n_results)
    if verbose:
        print("the query is", query, "and the results are", keyword_results)
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

def rank_relevant_outputs(self, series_list:List[SeriesForSearch], query:str) -> SeriesForSearch:
    instructor
    try:
    
        return self.groq_instructor_client.chat.completions.create(response_model=ClassifiedSeries, messages=[
            {"role": "system", "content": "You will be given a number of economic series from the user. Your job is to mark them as relevant or irrelevant for a given query and output it in the given format"}, {
                "role": "user", "content":f"The user's query is {query}. The possible datasets are {series_list}"
            }
        ], model="llama3-70b-8192")
    except Exception:
        return rank_relevant_outputs(series_list=series_list, query=query) 
