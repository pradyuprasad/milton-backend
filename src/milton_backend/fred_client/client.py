import requests

class FredAPIClient:
    base_url = "https://api.stlouisfed.org/fred"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def _api_call(self, endpoint: str, **kwargs):
        """
        General method to call FRED API endpoints.
        Parameters:
            endpoint (str): The FRED API endpoint to hit (e.g., 'series/observations').
            **kwargs: Arbitrary keyword arguments, defaulting to JSON format. These include:
                - file_type (str): Format of the output ('xml', 'json'). Default is 'json' on our end. Without specifying, the FRED API will give you XML.
                - limit (int): Maximum number of results to return.
                - sort_order (str): Order of the results ('asc', 'desc').
                - order_by (str): Attribute by which to order the results (e.g., 'series_count', 'popularity').
                - tag_names (str): Filter tags by names (applicable in some endpoints).
                - observation_start (str): Start of the observation period.
                - observation_end (str): End of the observation period.
        Returns:
            dict: JSON response from the FRED API.
        """
        params = {'api_key': self.api_key, 'file_type': 'json'}  # Default file_type set to 'json'
        params.update(kwargs)
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_tags(self, **kwargs):
        """
        Retrieve FRED tags with optional filtering.
        Keyword Arguments:
            limit (int): Maximum number of results to return.
            tag_names (str): Filter tags by names, semicolon delimited.
            order_by (str): Attribute to order results by, such as 'name', 'group_id', or 'popularity'.
            sort_order (str): 'asc' or 'desc' (default: 'asc').
        Returns:
            JSON response containing tags.
        """
        return self._api_call('tags', **kwargs)

    def get_series_by_tags(self, **kwargs):
        """
        Retrieve series that match all specified tags and exclude certain tags.
        Keyword Arguments:
            tag_names (str): Required. Semicolon delimited list of tag names that series must match.
            exclude_tag_names (str): Optional. Semicolon delimited list of tag names to exclude from results.
            order_by (str): Attribute to order results by, such as 'title', 'units', or 'frequency'.
            sort_order (str): 'asc' or 'desc'.
        Returns:
            JSON response containing series that match the criteria.
        """
        return self._api_call('tags/series', **kwargs)

    def get_observations(self, series_id, **kwargs):
        """
        Retrieve observations for a specific series.
        Parameters:
            series_id (str): The identifier for the series.
        Keyword Arguments:
            limit (int): Maximum number of results to return.
            order_by (str): Attribute to order results by, typically 'date' or 'realtime_start'.
            sort_order (str): 'asc' or 'desc' (default: 'asc').
        Returns:
            JSON response containing observations for the specified series.
        """
        return self._api_call('series/observations', series_id=series_id, **kwargs)

